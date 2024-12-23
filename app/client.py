import grpc
from protobufs import dictionary_pb2, dictionary_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = dictionary_pb2_grpc.DictionaryStub(channel)
        # Fetch a term
        response = stub.GetTerm(dictionary_pb2.GetTermRequest(name='Widget'))
        print(f"Term: {response.term.name}\nDescription: {response.term.description}")
        # List terms
        response = stub.ListTerms(dictionary_pb2.Empty())
        for term in response.terms:
            print(f"Term: {term.name}\nDescription: {term.description}\n")

if __name__ == '__main__':
    run()
