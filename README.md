# Redis Poke Service

## Project Description

Redis Poke Service is a Flask application designed to keep a Redis Cache instance active on Azure's free tier. The primary objective is to prevent service suspension due to inactivity by performing a "poke" every **2 minutes**.

## Requirements

- **Language:** Python 3.7+
- **Services:** Redis, Azure App Service
- **Python Dependencies:** Flask, redis, APScheduler

## Local Setup

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/redis-poke-service.git
    ```
2. **Navigate to the Project Directory:**
    ```bash
    cd redis-poke-service
    ```
3. **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Configure Environment Variables:**
    Create a `.env` file in the root of the project and add the following variables:
    ```
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_USER=default
    REDIS_PASSWORD=your_password
    REDIS_DB=0
    ```

## Deployment on Azure App Service

### 1. Create an Azure App Service

- Log in to the [Azure Portal](https://portal.azure.com/).
- Click on **"Create a resource"** and select **"App Service"**.
- Configure the App Service details:
  - **Name:** Choose a unique name for your app.
  - **Publish:** Code.
  - **Runtime stack:** Python 3.9.
  - **Region:** Select the region closest to you.
- Under **Service Plan**, select the **Free (F1)** tier.

### 2. Configure Environment Variables

- Navigate to your App Service instance.
- In the sidebar, select **"Configuration"**.
- Under **"Application settings"**, add the following variables:
  - `REDIS_HOST`
  - `REDIS_PORT`
  - `REDIS_USER`
  - `REDIS_PASSWORD`
  - `REDIS_DB`
- Enter the appropriate values for each variable.

### 3. Enable "Always On"

- In the App Service dashboard, go to **"Configuration" > "General settings"**.
- Locate the **"Always On"** option and set it to **"On"**.
- This ensures that the application remains continuously active, preventing suspension due to inactivity.

### 4. Configure Health Checks

- In the App Service dashboard, select **"Health check"**.
- Set the health check endpoint to `/healthcheck`.
- Configure the check interval to **5 minutes**.
- Save the settings.

### 5. Deploy the Application

- **Method 1: GitHub Actions**
  - Set up a GitHub Actions workflow to automatically deploy the application on every push.
- **Method 2: FTP**
  - Use the FTP credentials provided by Azure to manually upload the project files.

## Running the Application

After configuring and deploying the application, Azure App Service will automatically run the Flask application. The "poke" task will keep the Redis service active by updating the timestamp every **2 minutes** using a retry mechanism to ensure reliability.

## Monitoring and Logging

- **Log Stream:** Accessible from the Azure dashboard under **"Log stream"**, allows real-time log viewing.
- **Application Insights:** *(Optional)* Can be configured for enhanced visibility and advanced monitoring.

## Project Goal

The main goal of this project is to keep the Redis service active on Azure's free tier by preventing suspension due to inactivity. This is achieved by periodically performing a "poke" that updates a timestamp in the Redis database every **2 minutes**. Additionally, a **retry mechanism** has been implemented to enhance the reliability of Redis cache access, ensuring that transient errors do not disrupt the poke operations.

## Contributing

If you wish to contribute to this project, please create a pull request or open an issue describing the changes you would like to see.

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
