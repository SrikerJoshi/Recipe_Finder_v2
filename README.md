# Recipe_Finder_v2

## Project Description

This project implements a chatbot interface that provides detailed recipes with pretty images of the dishes and YouTube video links for the recipes. The chatbot interface is built using Streamlit and interacts with the Google Gemini LLM to fetch the recipes. The app now displays only images and searches until 5 images are found if the search results show gifs or videos. All images are displayed in the same size.


## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/SrikerJoshi/Recipe_Finder_v2.git
   cd Recipe_Finder_v2
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory and add the following lines to set up the environmental variables:
   ```bash
   GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key
   GOOGLE_API_KEY=your_google_api_key
   SEARCH_ENGINE_ID=your_search_engine_id
   PIXABAY_API_KEY=your_pixabay_api_key
   YOUTUBE_API_KEY=your_youtube_api_key
   GOOGLE_PLACES_API_KEY=your_google_places_api_key
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   IPINFO_Token=your_ipinfo_token
   ```

   Note: Keep the `.env` file private and do not share it.

5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Dependencies

- streamlit
- requests
- pillow
- langchain-google-genai
- langchain-community
- python-dotenv
- aiohttp
- asyncio
- google-api-python-client
- ipinfo

## Usage Instructions

1. Open the Streamlit app in your web browser.
2. Enter the name of the dish you want to cook in the text input field.
3. The chatbot will provide a detailed recipe, images of the dish, YouTube video links for the recipe, and restaurant locations serving the dish near you.
4. The app will now display only images and search until 5 images are found if the search results show gifs or videos. All images are displayed in the same size.

## Troubleshooting

- If the app fails to start, ensure that all dependencies are installed correctly.
- If you encounter any issues with fetching images, YouTube links, or restaurant locations, check your internet connection and ensure that your API keys are correct.
- If the app is not fetching images, YouTube links, or restaurant locations, try resetting the chat and starting again.

## Hosting Instructions

To host this app, you can use Streamlit Cloud or other hosting platforms. Here are the steps to host the app using Streamlight cloud:

1. Create a streamlet profile and connect click on Create an app and link your GitHub repository to the app.

2. Ensure all dependencies are listed in the `requirements.txt` file.

3. change the settings in streamlet app to be able to make the URL public for others to use the app.

4. Go to the app URL to start using the app.

## Hosting Instructions

### Steps to Host the App on GitHub

1. **Create a GitHub Repository:**
   - Go to [GitHub](https://github.com/) and sign in to your account.
   - Click on the "+" icon in the top right corner and select "New repository".
   - Enter a repository name, description (optional), and choose the visibility (public or private).
   - Click on "Create repository".

2. **Push the Code to GitHub:**
   - Open your terminal and navigate to the project directory.
   - Initialize a new Git repository:
     ```bash
     git init
     ```
   - Add the remote repository:
     ```bash
     git remote add origin https://github.com/your-username/your-repository-name.git
     ```
   - Add all files and commit:
     ```bash
     git add .
     git commit -m "Initial commit"
     ```
   - Push the code to the remote repository:
     ```bash
     git push -u origin main
     ```

3. **Set Up GitHub Actions for CI/CD:**
   - Create a `.github/workflows` directory in the project root.
   - Create a `deploy.yml` file inside the `.github/workflows` directory with the following content:
     ```yaml
     name: Deploy

     on:
       push:
         branches:
           - main

     jobs:
       build:
         runs-on: ubuntu-latest

         steps:
           - name: Checkout code
             uses: actions/checkout@v2

           - name: Set up Python
             uses: actions/setup-python@v2
             with:
               python-version: 3.12

           - name: Install dependencies
             run: |
               python -m pip install --upgrade pip
               pip install -r requirements.txt

           - name: Run Streamlit app
             run: |
               streamlit run app.py
     ```

4. **Configure GitHub Pages for Hosting:**
   - Go to the repository on GitHub.
   - Click on "Settings" and then "Pages" in the left sidebar.
   - Under "Source", select the branch you want to use for GitHub Pages (e.g., `main`).
   - Click "Save".

5. **Access the Hosted App:**
   - After the deployment is complete, you can access the hosted app using the GitHub Pages URL provided in the "Pages" settings.

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for more details.

## App Hosting Link

You can access the hosted app using the following link:

[Recipe Finder V 2.0](https://recipe-finder-v-02.streamlit.app/)
