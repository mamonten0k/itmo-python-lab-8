from concurrent import futures
import grpc

import dictionary_pb2
import dictionary_pb2_grpc

from models import Term as TermModel, Base
from database import SessionLocal, engine
from seed import seed_data
from sqlalchemy.orm import Session

def init_db():
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    seed_data(db_session)
    db_session.close()

class DictionaryService(dictionary_pb2_grpc.DictionaryServicer):
    def __init__(self):
        self.db: Session = SessionLocal()

    def AddTerm(self, request, context):
        existing_term = self.db.query(TermModel).filter(TermModel.name == request.term.name).first()
        if existing_term:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, f"Term '{request.term.name}' already exists.")
        new_term = TermModel(name=request.term.name, description=request.term.description)
        self.db.add(new_term)
        self.db.commit()
        return dictionary_pb2.TermResponse(term=request.term)

    def GetTerm(self, request, context):
        term = self.db.query(TermModel).filter(TermModel.name == request.name).first()
        if not term:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Term '{request.name}' not found.")
        return dictionary_pb2.TermResponse(term=dictionary_pb2.Term(name=term.name, description=term.description))

    def UpdateTerm(self, request, context):
        term = self.db.query(TermModel).filter(TermModel.name == request.name).first()
        if not term:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Term '{request.name}' not found.")
        term.description = request.description
        self.db.commit()
        return dictionary_pb2.TermResponse(term=dictionary_pb2.Term(name=term.name, description=term.description))

    def DeleteTerm(self, request, context):
        term = self.db.query(TermModel).filter(TermModel.name == request.name).first()
        if not term:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Term '{request.name}' not found.")
        self.db.delete(term)
        self.db.commit()
        return dictionary_pb2.DeleteTermResponse(message=f"Term '{request.name}' deleted successfully.")

    def ListTerms(self, request, context):
        terms = self.db.query(TermModel).all()
        response = dictionary_pb2.ListTermsResponse()
        for term in terms:
            response.terms.add(name=term.name, description=term.description)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dictionary_pb2_grpc.add_DictionaryServicer_to_server(DictionaryService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    init_db()
    serve()
