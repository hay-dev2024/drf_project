# from django.shortcuts import render
# from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView # Class basded views
from employees.models import Employee
from django.http import Http404
from rest_framework import mixins, generics


# Create your views here.
# Function Based Views
@api_view(['GET', 'POST'])
def studentsView(request):
    # manually serialise the 'QuerySet' using 'list()'; it's only for a simple task
    # students = Student.objects.all() # QuerySet
    # students_list = list(students.values())    

    # Serialiser: serialiser's a translator for your data
    # e.g. it converts 'QuerySet' -> 'JSON'
    if request.method == 'GET':
        # Get all the data from the Student table
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # when invalid
    
# everything's being handled in a single func
@api_view(['GET', 'PUT', 'DELETE'])    
def studentDetailView(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data) # pass the current student to update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Class Based Views
# CBV doesn't require decorators like @api_view()
# APIView takes care of a lot of things
# Employee List
# class Employees(APIView):
#     # create a member func get(). since this's a method, we need to pass in 'self'
#     def get(self, request):
#         employees = Employee.objects.all() # get all employees from the DB
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        

# # Employee Detail; CRUD
# class EmployeeDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         employee = self.get_object(pk) 
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     def put(self, request, pk):
#         employee = self.get_object(pk)
#         serialzier  = EmployeeSerializer(employee, data=request.data)
#         if serialzier.is_valid():
#             serialzier.save()
#             return Response(serialzier.data, status=status.HTTP_200_OK)
#         return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         employee = self.get_object(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# CBV with mixins
# mixins.ListModelMixin : fetches objects
# mixins.CreateModelMixin : creates objescts. in this case, an employee
# generics.GenericAPIView : handles GET, POST requests
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request) # list() is a func of ListModelMixin
    
    def post(self, request):
        return self.create(request) # create() is a func of CreateModelMixin
    
    
# mixins.RetrieveModelMixin : GET. fetches a single object
# mixins.UpdateModelMixin : PUT; UPDATE
# mixins.DestroyModelMixin : DELETE
class EmployeeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # retrieves a single employee from the DB
    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)

    