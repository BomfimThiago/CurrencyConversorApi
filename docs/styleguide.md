# Styleguide


**Table of contents:**

<!-- toc -->

- [Overview](#overview)
- [Core](#core-app)
- [App Independence and Code Reusability](#app-independence-and-code-reusability)
- [Models](#models)
  * [Base model](#base-model)
  * [Validation - `clean` and `full_clean`](#validation---clean-and-full_clean)
  * [Validation - constraints](#validation---constraints)
  * [Properties](#properties)
  * [Methods](#methods)
  * [Testing](#testing)
- [APIs](#apis)
  * [Views](#views)
  * [Serializers](#serializers)
  * [Use-cases](#use-cases)
  * [Docs](#docs)
  * [Testing](#testing-1)
 - [Urls](#urls)
 - [Services](#services)
 - [Utils](#utils)
 - [Exceptions](#exceptions)
 - [Settings](#settings)
 - [Enums](#enums)
 - [App Strucutre](#app-structure)
 - [Inspiration](#inspiration)

## Overview

The core of the Django Styleguide can be summarized as follows:

**In Django, business logic should live in:** ✅


- Use-cases - Classes that take care of writing and fetching things in the database
- Model properties (with some exceptions).
- Model `clean` method for additional validations (with some exceptions).
- Services - Additional abstraction layer that can be created if use-cases are having to much duplicated code.

**In Django, business logic should not live in:** ❌

- APIs and Views.
- Serializers and Forms.
- Form tags.
- Signals.


The general idea is to "separate concerns" so those concerns can be maintainable / testable.

**Services can be functions, classes, modules, or whatever makes sense for your particular case.**

With all that in mind, custom managers & querysets are very powerful tools and should be used to expose better interfaces for your models.


## Core App

The core app serves as the backbone of our project, containing essential components that are required across the entire application. It encompasses various functionalities, including Django settings, common code, abstractions, and utilities that can be shared and utilized by other apps within the project.


**Django Settings:**
The core app is the appropriate place to store Django settings that are common to the entire project. This helps in maintaining a centralized and consistent configuration.

**Common Code:**
The core app houses common code, such as base classes, mixins, and utility functions, which can be utilized by other apps. This approach reduces code duplication and promotes a DRY (Don't Repeat Yourself) codebase.

**Abstractions and Utilities:**
It provides abstractions and utilities that are widely applicable across different components of the project. These abstractions simplify complex functionalities and enhance code reusability.

**Dependency Management:**
Other apps within the project should ideally have imports only from the core app and themselves. By limiting dependencies to the core app and the app where the component is located, we can achieve a well-organized and modular project structure.


## App Independence and Code Reusability

In order to maintain a clear and modular codebase, it's important to prioritize app independence and code reusability. Here are guidelines to follow for achieving these goals:

**Independence Between Apps**
- Isolate App Functionality: Each app should encapsulate its specific functionality and not rely on imports from other apps. This ensures that apps remain independent and can be developed, tested, and maintained in isolation.
- Avoid Cross-App Imports: Refrain from importing code from outside your app unless it's from the core app. Cross-app imports can create tight coupling between apps, leading to maintenance challenges and potential conflicts.

**Reusable Code and Core App**
- Centralized Reusable Code Code snippets that are used across multiple apps should ideally be extracted to the core app. However, if duplication is necessary for app decoupling, it's acceptable to have some duplicated code.
- Specific Property in a Core Model: If you need to add a very specific property to a core model, utilize a [Proxy Model](https://docs.djangoproject.com/en/4.2/topics/db/models/#proxy-models). This approach extends the core model without altering its functionality.
```python
from core.models import User as CoreUser 

class User(CoreUser):
    def my_app_specific_property(self):
        ...

    class Meta:
        proxy = True
```
- Relationship with External Model: When creating a relationship with a model that's neither from your app nor from the core, consider using an [unmanaged model](https://docs.djangoproject.com/en/4.2/ref/models/options/#managed). This approach allows you to use the model without importing the original, avoiding unnecessary dependencies.
```python
class ModelName(BaseModel):
    essential_field = models.TextField()

    class Meta:
        managed = False
        db_table = 'original_app_model_name'

class ModelWhichNeedsRelationship(BaseModel):
    relation = models.ForeignKey(
        ModelName,
        ...
    )
    ...
```


## Models

Models should take care of the data model.

### Base model

It's a good idea to define a `BaseModel`, that you can inherit.

The current BaseModel sets the created, modified, and id of uuid type fields and resides in `/src/core/utils/models/base.py`


### Validation - `clean` and `full_clean`

Lets take a look at an example model:

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")
```

We are defining the model's `clean` method, because we want to make sure we get good data in our database.

Now, in order for the `clean` method to be called, someone must call `full_clean` on an instance of our model, before saving.

**Our recommendation is to do that in the use-case, right before calling save:**

```python
def course_create(name: str, start_date: date, end_date: date) -> Course:
    obj = Course(name=name, start_date=start_date, end_date=end_date)

    obj.full_clean()
    obj.save()

    return obj
```

This also plays well with Django admin, because the forms used there will trigger `full_clean` on the instance.

**We have few general rules of thumb for when to add validation in the model's `clean` method:**

1. If we are validating based on multiple, **non-relational fields**, of the model.
1. If the validation itself is simple enough.

**Validation should be moved to the use-case if:**

1. The validation logic is more complex.
1. Spanning relations & fetching additional data is required.

> It's OK to have validation both in `clean` and in the use-case, but we tend to move things in the use-case, if that's the case.

### Validation - constraints

If you can do validation using [Django's constraints](https://docs.djangoproject.com/en/dev/ref/models/constraints/), then you should aim for that.

Less code to write, less to code to maintain, the database will take care of the data even if it's being inserted from a different place.

Lets look at an example!

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
```

### Properties

Model properties are great way to quickly access a derived value from a model's instance.

For example, lets look at the `has_started` and `has_finished` properties of our `Course` model:

```python
...
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    ... 
    @property
    def has_started(self) -> bool:
        now = timezone.now()
        return self.start_date <= now.date()

    @property
    def has_finished(self) -> bool:
        now = timezone.now()
        return self.end_date <= now.date()
```

Those properties are handy, because we can now refer to them in serializers or use them in templates.

**We have few general rules of thumb, for when to add properties to the model:**

1. If we need a simple derived value, based on **non-relational model fields**, add a `@property` for that.
1. If the calculation of the derived value is simple enough.

**Properties should be something else (use-case, service, utility) in the following cases:**

1. If we need to span multiple relations or fetch additional data.
1. If the calculation is more complex.

Keep in mind that those rules are vague, because context is quite often important. Use your best judgement!


### Methods

Model methods are also very powerful tool, that can build on top of properties.

Lets see an example with the `is_within(self, x)` method:

```python
...

class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    ...

    def is_within(self, x: date) -> bool:
        return self.start_date <= x <= self.end_date
```

`is_within` cannot be a property, because it requires an argument. So it's a method instead.

Another great way for using methods in models is using them for **attribute setting**, when setting one attribute must always be followed by setting another attribute with a derived value.

An example:

```python
...

class Token(BaseModel):
    secret = models.CharField(max_length=255, unique=True)
    expiry = models.DateTimeField(blank=True, null=True)

    def set_new_secret(self):
        now = timezone.now()

        self.secret = get_random_string(255)
        self.expiry = now + settings.TOKEN_EXPIRY_TIMEDELTA

        return self
```

Now, we can safely call `set_new_secret`, that'll produce correct values for both `secret` and `expiry`.

**We have few general rules of thumb, for when to add methods to the model:**

1. If we need a simple derived value, that requires arguments, based on **non-relational model fields**, add a method for that.
1. If the calculation of the derived value is simple enough.
1. If setting one attribute always requires setting values to other attributes, use a method for that.

**Models should be something else (use-case, utility) in the following cases:**

1. If we need to span multiple relations or fetch additional data.
1. If the calculation is more complex.

Keep in mind that those rules are vague, because context is quite often important. Use your best judgement!

### Testing

Models need to be tested only if there's something additional to them - like validation, properties or methods.
Custom managers and querysets need to be tested.
The model,the manager  and the queryset tests, can be placed in a single file and should be placed in the same folder as the model.


## APIs

The APIs are versioned and they are separated in modules. their path should follow this format: `<app_name>.<v1|v2|v3>.<module_name>.<api_name>` e.g. `authentication.v1.reset_password.request_code`

**API Versioning**
Versioning is essential for maintaining backward compatibility and supporting API evolution over time.

**Module Organization**
Organize APIs into modules based on their related functionality. This approach promotes a cleaner project structure and makes it easier to locate and manage specific API components.

**Naming Conventions**
Adhere to consistent naming conventions for APIs, views, use-cases, and other components. Use descriptive names that reflect the purpose and functionality of each element.

**Each API consists of the following components:**

1. **View**: The view handles the incoming requests and returns the appropriate responses. It contains the logic for processing the requests and interacting with the underlying data models and use-cases.
1. **Use-cases**: Use-cases represent the business logic of the API. They encapsulate specific functionality and operations related to the API's purpose. Use-cases handle data validation, processing, and interactions with data sources like databases.
1. **Docs**: Documentation is essential for maintaining clear and comprehensive APIs. Each API should be thoroughly documented, providing details on the purpose, input parameters, expected outputs, and any error conditions. API documentation helps other developers understand how to interact with the API effectively.
1. **Tests**: Test cases ensure the correctness and reliability of APIs. For each API, comprehensive test suites should be created to cover various scenarios, including edge cases and error conditions. Automated tests help catch bugs early and maintain the stability of the API over time.
1. **Request and Response Serializers**: Request and response serializers help in data validation and transformation. They provide a structured way to validate incoming request data and serialize outgoing response data.


### Views

The view handles the incoming requests and returns the appropriate responses. It contains the logic for processing the requests and interacting with the underlying data models and use-cases.


**One View per Operation:**
For each CRUD operation on a model, have a separate API view. This means having four APIs for Create, Read, Update, and Delete operations. Keeping views focused on specific operations promotes better code organization and maintainability.

**Inheritance from Simple APIView or GenericAPIView:**
When creating new APIs, it is recommended to inherit from the simpler APIView or GenericAPIView rather than the more abstract classes. This approach allows us to manage data processing through use-cases rather than relying heavily on serializers.

**Separate Business Logic from Views:**
Avoid implementing business logic directly in views. Views should act as an interface to our core business logic. Instead, delegate business logic to use-cases to keep views clean and focused on handling HTTP requests and responses.

**Keep APIs Simple:**
Strive to keep APIs as simple as possible. Their primary purpose is to handle HTTP requests and responses, with the actual business logic residing in use-cases. Simple views are easier to read, test, and maintain.

**Consistent JSON Response Format:**
All views should respond with a JSON object containing at least a message string. Any calculated response data should be placed in an attribute named data, which can be of any type. If the response is paginated, the pagination metadata (total, current_page) should be added to the root of the response object.
```json
{
    "message": "The users listing was successful",
    "data": {
        "users": [
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Doe"}
        ]
    },
    "total": 2,
    "current_page": 1
}
```


**Pagination Example**

Pagination is handled by the pagination utils that reside in `src/core/utils/pagination`

```python
class UserListView(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    def get(self, request):
        request_serializer = UserListRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        response = UserListUseCase().execute(filters=request_serializer.validated_data)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=UserListResponseDataUserSerializer,
            queryset=users,
            request=request,
            view=self,
            message=AuthMessages.USER_LIST_SUCCESS.value,
        )
```


By following these guidelines, we can ensure that our views are well-organized, maintainable, and focused on their primary responsibility of handling HTTP requests and responses. Separating business logic into use-cases and maintaining a consistent JSON response format will result in clear and efficient APIs.


### Serializers
Serializers play a vital role in data validation and transformation for our APIs. They provide a structured approach to validate incoming request data and serialize outgoing response data. While serializers are optional, they are highly recommended, especially for complex APIs or those dealing with large amounts of data.

**Request and Response Separation::** Each API should have a dedicated request serializer and a dedicated response serializer. The request serializer handles incoming data, while the response serializer handles outgoing data.

**Serialization Abstraction:**
Choose an abstraction that best suits your needs for serialization. There are various serializers available in Django, and you can select the one that works most effectively for your specific use case.

**Location of Serializers:**
Place the serializers in the same folder as the corresponding API. This organization promotes a clearer project structure and makes it easier to locate related components.

**Unique Serializer Names:**
Avoid having two serializers with the same name, as this can impact the generation of OpenAPI documentation and lead to confusion.

**Preference for Simpler Serializer Inheritance:**
Our preference is for both request and response serializers to inherit from the simpler Serializer, rather than using ModelSerializer. However, this is a matter of choice, and if ModelSerializer works well for your situation, feel free to use it.

**Limited Serializer Reuse:**
Be cautious when reusing serializers. Reusing serializers may expose unexpected behavior if there are changes in the base serializers. It is generally better to create dedicated serializers for each API to maintain clarity and avoid potential issues.

**Naming Convention:**
Follow the naming convention <ApiName><Request|Response>Serializer. For instance, use SigninRequestSerializer and SigninResponseSerializer.


**Nesting Serializers:**
Nesting serializers can be easily archived with the inline_serializer helper that is located in `core.utils.serializer.inline_serializer`


Example
```python
class SignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)


class SignupResponseDataUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
        )


class SignupResponseSerializer(BaseResponseSerializer):
    data = inline_serializer(
        name="SignupResponseDataSerializer",
        fields={"user": SignupResponseDataUserSerializer()},
    )
```


Please note that serializers are also crucial in the **automatic generation of the OpenAPI documentation for our APIs**. By following the guidelines above, we ensure that the generated documentation accurately represents the structure and data handling of our APIs. Well-designed serializers contribute to clearer data handling and enhance the overall quality of our API implementations and documentation.

### Use-cases

Use-cases represent the core of our business logic and encapsulate specific functionalities within the software. They serve as the bridge between the application's domain language and various system components, allowing access to databases, other resources, and interaction with different parts of the system.

**Type Annotations:**
Use-cases are type-annotated, providing clear information about the input and output data, even if you are not using mypy at the moment.

**Documentation:**
Each use-case should have a docstring that explains its purpose, input parameters, and expected output. Well-documented use-cases help other developers understand their functionality and usage.

**Interaction with Resources:**
Use-cases can interact with the database, access other resources, and communicate with external services or tasks. They encapsulate complex business logic, from simple model creation to handling cross-cutting concerns.

**Inherits from BaseUseCase:**
All use-cases should inherit from BaseUseCase, which provides essential common functionality and ensures consistency across use-cases.

**Location:**
Use-cases should reside in the same folder as the API that uses them. This organization promotes a clearer project structure and makes it easier to locate related components.

**Filtering Example**

In this example, we showcase a use-case that leverages the powerful [django-filter](https://django-filter.readthedocs.io/en/stable/) library for filtering data.

```python
class FilterArgs(TypedDict):
    id: str | None
    email: str | None
    is_admin: bool | None

class UserListUseCase(BaseUseCase):
    class BaseUserFilter(django_filters.FilterSet):
        class Meta:
            model = User
            fields = ('id', 'email', 'is_admin')
    
    def execute(self, filters: FilterArgs = None) -> list[dict]:
        """
        List database users that match the filters
        Params:
            Filters: properties that the retrieved users need to match
        Returns: List of users
        """
        filters = filters or {}
        qs = User.objects.all()
        return self.BaseUserFilter(filters, qs).qs
```

### Docs


Proper documentation is essential for every endpoint in our application. It ensures that developers understand the API's functionality, allowed requests, possible responses, and expected data formats. We use the [drf_spectacular](https://drf-spectacular.readthedocs.io/en/latest/) package to generate the OpenAPI documentation automatically. The OpenAPI documentation page is accessible by default at the `/docs` path.

**Consistency with Serializers:**
The OpenAPI page should be consistent with the serializers used in our views. This ensures that the API documentation accurately reflects the request and response structures.

**Endpoint Documentation:**
Each endpoint in the OpenAPI documentation needs to include details about the allowed requests, possible responses, and relevant response examples. Use the `@extend_schema` decorator to link the documentation to the corresponding view.

**Use of Tags:**
To group related endpoints, we use tags in the OpenAPI documentation. Tags help in categorizing endpoints under appropriate sections, making it easier for developers to navigate and understand the API.

**File Naming Convention:**
For each view, create a corresponding doc.py file in the same folder. This file contains the documentation details for the specific view.


**Example** 

docs.py
```python
WRONG_CREDENTIALS_RESPONSE = OpenApiExample(
    AuthMessages.WRONG_CREDENTIALS.value,
    value={"detail": AuthMessages.WRONG_CREDENTIALS.value},
    response_only=True,
    status_codes=["401"],
)


docs = {
    "request": SigninRequestSerializer,
    "responses": {
        status.HTTP_200_OK: SigninResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
    },
    "summary": "Sign in",
    "tags": [Tags.AUTHENTICATION.value],
    "examples": [WRONG_CREDENTIALS_RESPONSE],
}
```
views.py
```python
...
class Signin(APIView):
    @extend_schema(**docs)
    def post(self, request: Request) -> Response:
        ...
```


### Testing

Testing is a critical aspect of our development process to ensure the reliability and correctness of our endpoints. We employ `pytest`, a popular testing framework, for writing integration tests.

**Integration Testing:**
Our testing focuses on integration testing, which evaluates the behavior of the entire system and ensures that all components work seamlessly together. Integration tests encompass testing endpoints and their interactions with use-cases, models, services, and other components.

**Testing Structure and Naming:**
Place the endpoint tests in the same folder as the corresponding view.
Follow the naming pattern `tests_<module_name>_<action>.py`. For example, `tests_user_list.py` for testing the "user list" endpoint.

**Test Coverage and Scenarios:**
Test for various scenarios, including edge cases and exceptions. Make sure to use different requests, Ensure that the use-cases and services have a test coverage of 100% to guarantee robustness and avoid any unnoticed issues.

**Assertions:**
Assertions are crucial in our tests. For each test case, we should assert the response status code, message, data, and the operations to ensure that the endpoint behaves as expected.

**Fixtures:**
To reduce code duplication, consider using fixtures. If a similar fixture is used in different files, move it to the conftest.py file. The [factoryboy](https://factoryboy.readthedocs.io/en/stable/index.html) library can be employed to generate random models in fixtures.

**Mocking:**
Always mock external calls to isolate the testing environment. When necessary, it is acceptable to mock 3rd party calls to prevent dependencies on external services during testing.

## Urls

We usually organize our urls the same way we organize our APIs - 1 url per API, meaning 1 url per action.

A general rule of thumb is to split urls from different domains in their own `domain_patterns` list & include from `urlpatterns`.

Here's an example with the APIs from above:

```python
from django.urls import path, include

from project.education.apis import (
    CourseCreateApi,
    CourseUpdateApi,
    CourseListApi,
    CourseDetailApi,
    CourseSpecificActionApi,
)


course_patterns = [
    path('', CourseListApi.as_view(), name='list'),
    path('<int:course_id>/', CourseDetailApi.as_view(), name='detail'),
    path('create/', CourseCreateApi.as_view(), name='create'),
    path('<int:course_id>/update/', CourseUpdateApi.as_view(), name='update'),
    path(
        '<int:course_id>/specific-action/',
        CourseSpecificActionApi.as_view(),
        name='specific-action'
    ),
]

urlpatterns = [
    path('courses/', include((course_patterns, 'courses'))),
]
```

**Splitting urls like that can give you the extra flexibility to move separate domain patterns to separate modules**, especially for really big projects, where you'll often have merge conflicts in `urls.py`.

Now, if you like to see the entire url tree structure, you can do just that, by not extracting specific variables for the urls that you include.

**The urls are versioned**, and this requires the urls to be propagated through different files until it finnally being declared in `core/urls.py`

## Services

To minimize code duplication and promote reusability, it is recommended to create a services folder in the root directory of your app.

A service in our context can be defined as a function, a class, or even an entire module that encapsulates specific functionalities that are utilized across multiple components of the application.


**Code Reusability:**
Services act as an abstraction layer that centralizes common functionalities. They allow us to reuse code in various parts of the application, reducing duplication and promoting a DRY (Don't Repeat Yourself) codebase.

**Separation of Concerns:**
By abstracting common functionalities into services, we keep our use-cases, models, and other components focused on their specific tasks. Services handle shared functionalities, making the codebase more organized and maintainable.

**Interaction with Multiple Components:**
Services can be called from use-cases, models, views, or even other services. This flexibility allows for smooth communication between different parts of the application.

**Examples of Services:**
A service could encompass tasks such as:

1. File handling and storage.
1. Sending notifications and emails.
1. External API interactions and data retrieval.
1. Complex data calculations or transformations.
1. Data validation and sanitization.

**Service Location:**
Place the service files within the services folder in the app's root directory. This location ensures easy access and discoverability.

**Note:**

While services provide a powerful way to promote code reusability and maintain a modular codebase, avoid excessive use of services for every small functionality. Reserve their use for functionalities that are genuinely shared across the application to maintain a clean and organized architecture.

## Utils

The utils reside in a folder named `utils` in the app root folder is dedicated to housing utility functions and helper modules that provide common functionalities across the application. It serves as a centralized location for storing reusable code.


**Example:**:
```python 
from datetime import datetime

def format_date_to_string(date):
    return date.strftime("%Y-%m-%d")
```

## Exceptions

In our application, exceptions play a crucial role in providing meaningful error handling and communication between different components. To maintain consistency and clarity, we organize app exceptions in a dedicated folder named exceptions. Each exception should extend a core exception to ensure a standardized approach.


**Core Exception Inheritance:**
All app exceptions should inherit from an exception from rest_framework.exceptions, which can provide a unified base for error handling.

**Exception Details and Error Codes:**
Exceptions should contain detailed information about what happened and an error code that assists the frontend in handling the error gracefully. These messages and codes can be defined in the enums folder for easy reference and consistency.

**HTTP Status Codes:**
Exceptions must follow the REST API HTTP status codes. Always strive to use appropriate status codes to accurately reflect the nature of the exception.

**Avoiding 500 Errors:**
It is crucial to avoid returning generic 500 Internal Server Error responses. Instead, use specific exceptions to provide clear and actionable feedback to the clients.

**Example:**
```python
class UserNotFound(NotFound):
    def __init__(self, detail=AuthMessages.USER_NOT_FOUND.value):
        super().__init__(detail, ErrorCodes.USER_NOT_FOUND.value)
```

**Minimum Encapsulation:** Encapsulate the minimum amount of code in try...except blocks. This ensures that only the specific code that is prone to exceptions is enclosed, rather than wrapping the entire block.

**Avoid Generic Exception:** Avoid using the generic Exception class in the except statement. Instead, catch specific exceptions that you expect to occur. This allows for better error identification and handling, as different exceptions can be addressed in distinct ways.

```python
# Avoid: ❌❌❌
try:
    # Some code that might raise an exception
except Exception as e:
    # Handle the exception


# Prefer: ✅✅✅
try:
    # Some code that might raise an exception
except SpecificException as e:
    # Handle the specific exception
```

## Enums

The enums folder serves as a centralized location to store constants that are meant to be used throughout the codebase. These constants can include error codes, response messages, documentation tags, and any other fixed values that are used in multiple places.

**Example structure:**
```
my_app/
    ├── enums/
    │   ├── error_codes.py
    │   ├── response_messages.py
    │   ├── documentation_tags.py
    │   └── ...
    └── ...
```


## App structure

**Modules Structure:**

For components that require multiple related files, create a dedicated folder with a descriptive name to group them together.
To improve access to related files, import them in a __init__.py file within the folder.

**App structure example**

```
.
├── admin.py
├── enums
│   ├── __init__.py
│   ├── codes.py
│   ├── docs.py
│   └── messages.py
├── exceptions
│   ├── __init__.py
│   ├── jwt.py
│   └── user.py
├── middlewares.py
├── migrations
│   ├── __init__.py
│   └── 0001_initial.py
├── models
│   ├── user
│   │   ├── __init__.py
│   │   ├── managers.py
│   │   ├── test_user.py
│   │   └── models.py
│   └── __init__.py
├── services
│   ├── __init__.py
├── utils
│   ├── __init__.py
│   ├── jwt.py
│   └── secrets.py
├── v1
│   ├── users
│   │   ├── get
│   │   │   ├── __init__.py
│   │   │   ├── docs.py
│   │   │   ├── serializers.py
│   │   │   ├── tests_get_user.py
│   │   │   ├── use_case.py
│   │   │   └── views.py
│   │   ├── list
│   │   │   ├── __init__.py
│   │   │   ├── docs.py
│   │   │   ├── serializers.py
│   │   │   ├── tests_list_users.py
│   │   │   ├── use_case.py
│   │   │   └── views.py
│   ├── __init__.py
│   └── urls.py
├── __init__.py
├── apps.py
├── conftest.py
├── permissions.py
└── urls.py
```


## Best Practices


**Queries Optimization:**
Always look for opportunities to optimize database queries. Use the debug toolbar to identify and resolve (N + 1) query issues. Review the debug toolbar output for each endpoint to ensure efficient database operations.

**Versioning and Commit guidelines**
1. Conventional Commits: Use [conventional commits](https://cheesecakelabs.atlassian.net/wiki/spaces/WIKI/pages/1962377244/Conventional+Commits) that clearly convey the purpose of each commit. Ensure that the commit messages are descriptive and meaningful.
1. Every commit should be a perfect, atomic unit of change, so always avoid commits like: `style: fix lint`, use pre-commit to make sure that your commit is in a working state
1. Jira Integration: Set up GJira integration to link commit messages with Jira tickets. Assign ticket descriptions to commits to maintain a clear history of code changes.
1. Git Flow: Follow the Gitflow workflow for branch management, making it easier to manage features, releases, and hotfixes.
1. Continuous Integration (CI): Make sure that the CI workflow is set in the repository. The CI pipeline should include checks for running tests and code quality tools to ensure that all changes adhere to project standards.


**Code Quality:**

1. Code Formatting: Use code formatting tools like isort and black to ensure consistent and readable code. These tools automatically sort imports and format the code to match the style guide.
1. Style Guide Enforcement: Utilize flake8 to enforce the project's style guide. Make sure the code adheres to the defined guidelines for consistency.
1. Type Checking: Use MyPy to perform static type checking, helping to catch typing errors and improve code correctness.
1. Function Documentation: Feel free to include docstrings for functions and methods to provide clear documentation for their purpose and usage. Keep the docstrings up-to-date along with the code changes.
Add as many types as you can to help to make your functions more readable. Feel free to add docstrings to your functions too, and make sure they are always updated along with the code.

**Makefile**
Makefile Commands: Maintain a comprehensive Makefile that includes all the commonly used commands for the project. Add instructions on how to use these commands in the project's README. Always ensure that the Makefile commands are tested and functional. Verify that each command runs without errors.

**Docker**
Docker is how the project will run on production. Ensure that the Docker version of the project is working as expected.

**ERD**
Use Django Extensions to generate an Entity-Relationship Diagram (ERD) for the project's database schema. Include the ERD in the project's README and keep it updated.

**Logging**
Always initialize loggers using the logging module. Create logger instances with specific names that correspond to the module or context they are used in. Utilize different logging levels (debug, info, warning, error, critical) based on the severity of the log message.

```python
import logging

logger = logging.getLogger("logger_name")

logger.info("This is an informational message")
logger.warning("This is a warning message")
logger.error("This is an error message")
```

With these in mind, avoid `print` statements and always log exceptions

**Setup Sentry**
Set up Sentry for error tracking and monitoring. Set the SENTRY_DSN environment variable in the project to enable Sentry reporting. Once the SENTRY_DSN is set, Sentry automatically captures unhandled exceptions and errors in your code.


## Inspiration


This starter is inspired by [Django styleguide](https://github.com/HackSoftware/Django-Styleguide/) and this documentation was created with the help of [ChatGPT](https://chat.openai.com/)
