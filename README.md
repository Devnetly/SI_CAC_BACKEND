# CAC Backend

## Setup


1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    - For Windows:

      ```bash
      venv\Scripts\activate
      ```

    - For macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

3. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Run the Django Server

1. Follow `.env.template` to setup your database settings in the `.env`


2. Apply database migrations:

    ```bash
    python manage.py makemigrations
    ```

    ```bash
    python manage.py migrate
    ```

3. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

4. Open your web browser and visit [http://localhost:8000](http://localhost:8000) to access the application.

## Additional Notes

- If you need to deactivate the virtual environment, simply run:

  ```bash
  deactivate
  ```

- For more information on Django, refer to the [official documentation](https://docs.djangoproject.com/).
