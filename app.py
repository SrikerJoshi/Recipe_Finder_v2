import streamlit as st
import aiohttp
import asyncio
import ipinfo
from PIL import Image
from io import BytesIO
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv


# Load environment variables from a .env file
load_dotenv()

api_key = os.getenv("GOOGLE_GEM_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")
pix_key = os.getenv("PIXABAY_API_KEY")
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
ipinfo_token = os.getenv("IPINFO_TOKEN")

# Initialize the Google Gemini LLM
llm = GoogleGenerativeAI(model="gemini-1.5-flash-8b-exp-0924", google_api_key=api_key)

# Reset context functionality
if 'chat' not in st.session_state:
    st.session_state.chat = llm  # Initialize chat context

# Reset chat function
def reset_chat():
    st.session_state.chat = llm  # Reset chat context
    st.session_state.recipe = ""  # Reset recipe
    st.session_state.images = []   # Reset images
    st.session_state.youtube_links = ""  # Reset YouTube links
    st.session_state.images_requested = False  # Reset images request status
    st.session_state.locations = []  # Reset locations
    st.session_state.locations_requested = False  # Reset locations request status

# Improved recipe fetching
def get_recipe(dish_name):
    try:
        prompt = f"Please provide a detailed recipe for {dish_name}. Be a helpful assistant."
        response = st.session_state.chat.generate([prompt])  # Ensure it's passed as a list
        return response.generations[0][0].text if response.generations else 'No recipe found.'
    except Exception as e:
        return f"Error fetching recipe: {e}"

# # If Gppgle LLM gets the capablity to get YouTube links, we can use this function
# def get_youtube_links(dish_name):
#     try:
#         prompt = f"Find 5 YouTube video links for the recipe of {dish_name}."
#         response = st.session_state.chat.generate([prompt])  # Ensure it's passed as a list
#         return response.generations[0][0].text if response.generations else 'No video link found.'
#     except Exception as e:
#         return f"Error fetching YouTube links: {e}"

# Improved YouTube link fetching using YouTube Data API
async def fetch_youtube_links(dish_name):
    try:
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={dish_name}&key={youtube_api_key}&maxResults=5&type=video"
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                response_data = await response.json()
        
        if 'items' in response_data and response_data['items']:
            video_links = []
            for item in response_data['items']:
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_links.append((title, video_url))  # Append title and URL
            return video_links  # Return a list of tuples (title, url)
        else:
            return 'No videos found.'  # Custom message when no videos are found
    except Exception as e:
        return f"Error fetching YouTube links: {e}"

   
# trying out Pixabay API for image fetching but its not accurate
# def get_images(dish_name):
#     try:
#         search_url = f"https://pixabay.com/api/?key={pix_key}&q={dish_name}&image_type=photo"
#         response = requests.get(search_url).json()       
#         if 'hits' in response and response['hits']:
#             image_urls = [item['webformatURL'] for item in response['hits'][:5]]
#             images = []
#             for url in image_urls:
#                 try:
#                     img = Image.open(BytesIO(requests.get(url).content))
#                     images.append(img)
#                 except Exception as e:
#                     st.warning(f"Error loading image from URL {url}: {e}")
#             return images
#         else:
#             return []
#     except Exception as e:
#         st.error(f"Error fetching images: {e}")
#         return []

# # Improved Image fetching function using LLM
# def get_images(dish_name):
#     try:
#         prompt = f"Provide 5 image URLs related to the dish '{dish_name}'."
#         response = st.session_state.chat.generate([prompt])  # Ensure it's passed as a list
#         # Access the generated text from the first generation
#         image_urls = response.generations[0][0].text.strip().split('\n') if response.generations else []
        
#         # Fetch images from URLs
#         images = []
#         for url in image_urls:
#             try:
#                 img = Image.open(BytesIO(requests.get(url).content))
#                 images.append(img)
#             except Exception as e:
#                 st.warning(f"Error fetching image from URL {url}: {e}")
        
#         return images
#     except Exception as e:
#         st.error(f"Error fetching images: {e}")
#         return []


# Async function to fetch images
async def fetch_images(dish_name):
    try:
        search_url = f"https://www.googleapis.com/customsearch/v1?q={dish_name}&searchType=image&key={google_api_key}&cx={search_engine_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                response_data = await response.json()
        
        images = []
        if 'items' in response_data:
            image_urls = [item['link'] for item in response_data['items']]
            # Create a new session to fetch images
            async with aiohttp.ClientSession() as session:
                tasks = []
                for url in image_urls:
                    tasks.append(fetch_image(session, url))  # Corrected function name to fetch_image
                images = await asyncio.gather(*tasks)
            
            # Filter out None values and ensure only images are included
            images = [img for img in images if img is not None]
            
            # Continue searching until 5 images are found
            while len(images) < 5 and 'queries' in response_data and 'nextPage' in response_data['queries']:
                next_page_url = f"https://www.googleapis.com/customsearch/v1?q={dish_name}&searchType=image&key={google_api_key}&cx={search_engine_id}&start={response_data['queries']['nextPage'][0]['startIndex']}"
                async with session.get(next_page_url) as next_response:
                    next_response_data = await next_response.json()
                    if 'items' in next_response_data:
                        next_image_urls = [item['link'] for item in next_response_data['items']]
                        next_tasks = [fetch_image(session, url) for url in next_image_urls]
                        next_images = await asyncio.gather(*next_tasks)
                        images.extend([img for img in next_images if img is not None])
            
            return images[:5]  # Return only the first 5 images
        
    except Exception as e:
        st.error(f"Error fetching images: {e}")
        return []

# Helper function to fetch a single image
async def fetch_image(session, url):  # Corrected function name to fetch_image
    try:
        async with session.get(url) as img_response:
            content_type = img_response.headers.get('Content-Type')
            if content_type and 'image' in content_type and 'gif' not in content_type:
                img = Image.open(BytesIO(await img_response.read()))
                return img
    except Exception as e:
        return None
    

async def fetch_locations(dish_name):
    try:        
        # Fetch locations using Google Places API
        places_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={dish_name}&key={google_places_api_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(places_url) as response:
                places_data = await response.json()
        
        locations = []
        if 'results' in places_data:
            locations = [(place['name'], place['geometry']['location']) for place in places_data['results'][:5]]
        
        return locations
    except Exception as e:
        return [], []


# Title and instructions
st.title("Recipe Finder Chatbot")
st.write("Learn how to cook delicious food with detailed recipes, images, and YouTube video links!")
st.write("Please be patient while the chatbot fetches the information for you.")
st.write("Please click Reset chat to reset the chat and start fresh.")

# Text input for dish name
dish_name = st.text_input("Enter the name of the dish you want to cook:")

# Initialize session state variables for recipe, images, and YouTube links
if 'recipe' not in st.session_state:
    st.session_state.recipe = ""
if 'images' not in st.session_state:
    st.session_state.images = []
if 'youtube_links' not in st.session_state:
    st.session_state.youtube_links = ""
if 'images_requested' not in st.session_state:
    st.session_state.images_requested = False
if 'locations' not in st.session_state:
    st.session_state.locations = []
if 'locations_searched' not in st.session_state:
    st.session_state.locations_searched = []


# Single button for fetching recipe, images, and YouTube links
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Get Recipe, Images, and YouTube Links"):
        if dish_name:
            with st.spinner("Fetching data..."):
                if st.session_state.locations_searched:
                    reset_chat()
                try:
                    st.session_state.recipe = get_recipe(dish_name)
                    st.session_state.images = asyncio.run(fetch_images(dish_name))
                    st.session_state.youtube_links = asyncio.run(fetch_youtube_links(dish_name))
                    st.session_state.images_requested = True
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
        elif st.session_state ==[] and dish_name == "":
            st.warning("Please enter a dish name first.")


# Button for showing Google Maps

with col2:
    if st.button("Restaurant serving this dish near you"):
        if dish_name:
            with st.spinner("Fetching data..."):
                if st.session_state.recipe is not None:
                    reset_chat()
                st.session_state.locations = asyncio.run(fetch_locations(dish_name))
                st.session_state.locations_searched = True


# Create a new row for the Reset Chat button
st.write("")  # Add a little space
reset_col1, reset_col2, reset_col3 = st.columns(3)
with reset_col2:
    if st.button("Reset"):
        reset_chat()
        st.write("Chat was reset successfully!")

#getting user location latitude and longitude based on their IP address to be able to show the restaurents near them.
def get_user_location():
    access_token = ipinfo_token 
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()
    location = details.loc.split(",")  # lat, long
    return float(location[0]), float(location[1])
user_latitude, user_longitude = get_user_location()

if st.session_state.locations:
    try:
        col = st.columns([1])
        with col[0]:
            st.markdown(f"""
                <iframe
                    width="100%"
                    height="500"
                    style="border:0" display: block; margin-left: auto; margin-right: auto;"  # Ensure centering of the iframe
                    loading="lazy"
                    allowfullscreen
                    src="https://www.google.com/maps/embed/v1/search?key={google_maps_api_key}&q={dish_name}&center={user_latitude},{user_longitude}&zoom=12">
                </iframe>
            """, unsafe_allow_html=True)
            st.subheader("Locations")
            for name, location in st.session_state.locations:
                st.write(f"{name}: {location}")  
    except Exception as e:
        st.error(f"Error fetching data: {e}")    
elif st.session_state == [] and dish_name == "":
    st.warning("Please enter a dish name.")




# Display Recipe
if st.session_state.recipe:
    st.subheader("Recipe")
    st.write(st.session_state.recipe)

# Display Images
if st.session_state.images:
    st.subheader("Images")
    
    # Create columns for displaying images side by side
    cols = st.columns(5)  # Create 5 columns (adjust as needed based on the number of images)

    for i, image in enumerate(st.session_state.images):
        with cols[i % 5]:  # Use modulo to wrap around to the first column after the fifth
            st.image(image, use_column_width='always', width=150)  # Set a fixed width
            st.markdown("<br>", unsafe_allow_html=True)  # Add a gap between images

else:
    # Show message only if images were requested
    if st.session_state.images_requested:
        st.write("No images found.")


# Display YouTube Video Links
if st.session_state.youtube_links:
    st.subheader("YouTube Videos")
    youtube_links = st.session_state.youtube_links 
    if isinstance(youtube_links, list) and youtube_links:
        for title, link in youtube_links:
            st.markdown(f"[{title}]({link.strip()})", unsafe_allow_html=True)
    elif youtube_links == 'No videos found.':  # Check for the custom message
        st.write(youtube_links)  # Display the custom message
    else:
        st.write("Error fetching YouTube links.")
