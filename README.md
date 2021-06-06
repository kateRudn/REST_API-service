A simple REST API is a multi-user service for users to work with their data. Supports the following endpoints: 
- registration of new users, 
- authorization of existing users, 
- viewing a list of their jokes for the user,
- getting a joke by id,
- adding a new joke,
- generating a joke on a public service and adding it to the list of jokes,
- updating a joke by id,
- deleting a joke by id.

Commands:

1. User registration
curl -i -u <USERNAME>:<PASSWORD> -X POST http://localhost:5000/registration

2. Getting a list of the user's jokes
curl -i -u <USERNAME>:<PASSWORD> http://localhost:5000/jokes

3. Getting a joke by id
curl -i -u <USERNAME>:<PASSWORD> http://localhost:5000/jokes/<IDJOKE>

4. Adding your own joke
curl -i -u <USERNAME>:<PASSWORD> -H "Content-Type: application/json" -X POST -d "{""joke"":""<TEXTOFJOKE>""}" http://localhost:5000/jokes/create

5. Generating joke
curl -i -u <USERNAME>:<PASSWORD> -X POST http://localhost:5000/jokes/generate

6. Updating joke by id
curl -i -u <USERNAME>:<PASSWORD> -H "Content-Type: application/json" -X PUT -d "{""joke"":""<TEXTOFJOKE>""}" http://localhost:5000/jokes/<IDJOKE>

7. Deleting joke by id
curl -i -u <USERNAME>:<PASSWORD> -X DELETE http://localhost:5000/jokes/<IDJOKE>
