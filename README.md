
# OnlyDrive

OnlyDrive is a Django-based project that acts as Cloud Storage, where you can perform some simple operations on your files.


## Tech Stack

**Client:** HTML, CSS, JavaScript, Bootstrap (CloudBox Lite by Iqonic Design)

**Server:** Django, SQLite


## Features

- Uploading Files
- Creating folders to help you manage your files
- Renaming / deleting files
- Renaming / deleting folders
- Downloading single files
- Download all files in specific folder as .zip
- Dashboard that shows most recent files and folder with most files
- API (description below) & API Key management

## Run Locally

Clone the project

```bash
  git clone https://github.com/RaiseCreed/OnlyDrive.git
```

Go to the project directory

```bash
  cd OnlyDrive
```

Create your virtual environment 

```bash
  pip install virtualenv
  virtualenv envname
```

Activate virtual environment 

```bash
  envname\scripts\activate
```

Install the requirements

```bash
  pip install -r requirements.txt
```

Run the app

```bash
  python manage.py runserver
```

> ⚠ Server will be started at http://127.0.0.1:8000/


**Default user is 'admin' and password is 'passwordForAdmin'**


## API Reference

This API uses Django REST Framework API Key module for authorization. All API calls must be authorized with 
```http
Authorization: Api-Key <API_KEY>
```
header, where <API_KEY> is your key generated from the app. OnlyDrive allows you to generate API keys that are restricted to specific request types (one or many).

#### Get all files

Returns all files uploaded by current user

```http
  GET /api/files
```

#### Get item

Returns info about specific file

```http
  GET /api/files/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of file to fetch |

#### Get all folders

Returns all files uploaded by current user

```http
  GET /api/folders
```

#### Get folder

Returns info about specific folder

```http
  GET /api/folders/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of folder to fetch |

#### Get files from folder

Returns files inside a specific folder

```http
  GET /api/folders/${id}/files
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of a folder |

#### Get storage info

Returns information about storage space

```http
  GET /api/driveinfo
```

#### Delete file

Deletes specific file

```http
  DELETE /api/files/${id}/delete
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of a file |

#### Edit file

Edits specific file. You can edit name and folder. 

```http
  PATCH /api/files/${id}/edit
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of a file |


Body of a request should be sent as JSON:
```json
{
    "name":"<new_filename> - Optional",
    "folder":"<id_of_assigned_folder> - Optional"
}
```

#### Download file

Downloads specific file

```http
  GET /api/files/${id}/download
```
## Screenshots

![login](https://github.com/RaiseCreed/OnlyDrive/assets/104384996/c8e0379e-e852-49c7-b31a-c6e35df6a3b1)
![dashboard](https://github.com/RaiseCreed/OnlyDrive/assets/104384996/22be9169-01c4-48e2-af9d-d090cadd4691)
![files](https://github.com/RaiseCreed/OnlyDrive/assets/104384996/3db4b66f-fcdb-481f-a791-63cccd2920eb)
![folders](https://github.com/RaiseCreed/OnlyDrive/assets/104384996/b3793dad-4005-4334-825e-63af0ee1f29c)
![keys](https://github.com/RaiseCreed/OnlyDrive/assets/104384996/22942d15-a4d5-4fc7-a8bb-1aa3886aae03)
![one-folder](https://github.com/RaiseCreed/OnlyDrive/assets/104384996/8f4176ba-f939-4cba-9a36-3342009565bb)

