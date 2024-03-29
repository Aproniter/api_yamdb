# api_yamdb
api_yamdb

<h1 align="center">YaMDB API</h1>

### Description
������ YaMDb �������� ������ ������������� �� ��������� ������������.
������������ ������� �� ���������, ������� ����� ����������� ��� ���������.
� ������� ������������ ��������� ���������������� �����:
- ������ � ����� ������������� �������� ������������, ������ ������ � �����������.
- ������������������� ������������ (user) � �����, ��� � ������, ������ ��, ������������� �� ����� ����������� ������ � ������� ������ ������������� (�������/������/��������), ����� �������������� ����� ������; ����� ������������� � ������� ���� ������ � �����������. ��� ���� ������������� �� ��������� ������� ������ ������������.
- ��������� (moderator) � �� �� �����, ��� � � �������������������� ������������ ���� ����� ������� ����� ������ � �����������.
- ������������� (admin) � ������ ����� �� ���������� ���� ��������� �������. ����� ��������� � ������� ������������, ��������� � �����. ����� ��������� ���� �������������.

**YaMDB API**
### ������� ������ � API ��� ���� �������������
��������� ������������ �������� �� ������ /redoc/
��� ���������������� ������������� ������ � API �������� � ������ ������.

```
����� �������: �������� ��� ������.
GET /api/v1/categories/ - ��������� ������ ���� ���������
GET /api/v1/genres/ - ��������� ������ ���� ������
GET /api/v1/titles/ - ��������� ������ ���� ������������
GET /api/v1/titles/{title_id}/reviews/ - ��������� ������ ���� �������
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - ��������� ������ ���� ������������ � ������

����� �������: �������������
GET /api/v1/users/ - ��������� ������ ���� �������������
```


### ����������� ������ ������������
�������� ��� ������������� �� ���������� email.
����� �������: �������� ��� ������.
������������ ��� 'me' � �������� username ���������.
���� email � username ������ ���� �����������.

����������� ������ ������������:
```
POST /api/v1/auth/signup/

{
  "email": "string",
  "username": "string"
}
```

��������� JWT-������:
```
POST /api/v1/auth/token/

{
  "username": "string",
  "confirmation_code": "string"
}
```

### ������� ������ � API ��� �������������� �������������
���������� ���������:
```
����� �������: �������������.
POST /api/v1/categories/

{
  "name": "string",
  "slug": "string"
}
```

�������� ���������:
```
����� �������: �������������.
DELETE /api/v1/categories/{slug}/
```

���������� �����:
```
����� �������: �������������.
POST /api/v1/genres/

{
  "name": "string",
  "slug": "string"
}
```

�������� �����:
```
����� �������: �������������.
DELETE /api/v1/genres/{slug}/
```

���������� ����������:
```
PUT /api/v1/posts/{id}/

{
"text": "string",
"image": "string",
"group": 0
}
```

���������� ������������:
```
����� �������: �������������. 
������ ��������� ������������, ������� ��� �� �����.
POST /api/v1/titles/

{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

���������� ������������:
```
����� �������: �������� ��� ������
GET /api/v1/titles/{titles_id}/

{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

��������� ���������� ���������� � ������������:
```
����� �������: �������������
PATCH /api/v1/titles/{titles_id}/

{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

��������� ���������� ���������� � ������������:
```
����� �������: �������������
DEL /api/v1/titles/{titles_id}/
```


### ������ � ��������������:
��� ������ � ������������ ���� ��������� ����������� ��� ������ � ����.
��������� ������ ���� �������������.
```
����� �������: �������������
GET /api/v1/users/ - ��������� ������ ���� �������������
```
���������� ������������:
```
����� �������: �������������
POST /api/v1/users/ - ���������� ������������

{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
��������� ������������ �� username:
```
����� �������: �������������
GET /api/v1/users/{username}/ - ��������� ������������ �� username
```
��������� ������ ������������ �� username:
```
����� �������: �������������
PATCH /api/v1/users/{username}/ - ��������� ������ ������������ �� username

{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

�������� ������������ �� username:
```
����� �������: �������������
DELETE /api/v1/users/{username}/ - �������� ������������ �� username
```
��������� ������ ����� ������� ������:
```
����� �������: �������������� ������������
GET /api/v1/users/me/ - ��������� ������ ����� ������� ������
```
��������� ������ ����� ������� ������:
```
����� �������: ����� �������������� ������������
PATCH /api/v1/users/me/ - ��������� ������ ����� ������� ������
```
