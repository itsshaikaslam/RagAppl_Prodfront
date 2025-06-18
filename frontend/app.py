#import streamlit as st
# import requests
# import json
# from datetime import datetime
# import pandas as pd
# import time
# from typing import List, Dict, Any

# # Constants
# #API_URL = "http://localhost:8000"
# API_URL =  "https://web-production-6ef03.up.railway.app"

# def format_file_size(size_bytes):
#     """Format file size in bytes to human readable format."""
#     for unit in ['B', 'KB', 'MB', 'GB']:
#         if size_bytes < 1024.0:
#             return f"{size_bytes:.2f} {unit}"
#         size_bytes /= 1024.0
#     return f"{size_bytes:.2f} TB"

# def format_date(date_str):
#     """Format ISO date string to readable format."""
#     try:
#         date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
#         return date.strftime('%Y-%m-%d %H:%M:%S')
#     except:
#         return date_str

# def handle_api_error(e, operation: str):
#     """Handle API errors consistently."""
#     if isinstance(e, requests.exceptions.ConnectionError):
#         st.error(f"Could not connect to the backend server. Please ensure it's running at {API_URL}")
#     elif isinstance(e, requests.exceptions.RequestException):
#         st.error(f"Error during {operation}: {str(e)}")
#     else:
#         st.error(f"Unexpected error during {operation}: {str(e)}")

# def list_files():
#     """List files from Google Drive."""
#     try:
#         response = requests.get(f"{API_URL}/files")
#         response.raise_for_status()
#         data = response.json()
#         if data["status"] == "ok":
#             return data["files"]
#         return []
#     except Exception as e:
#         st.error(f"Error listing files: {str(e)}")
#         return []

# def search_files(query: str):
#     """Search for files."""
#     try:
#         response = requests.get(f"{API_URL}/search", params={"query": query})
#         response.raise_for_status()
#         data = response.json()
#         if data["status"] == "ok":
#             return data["results"]
#         elif data["status"] == "warning":
#             st.warning(data["message"])
#         return []
#     except Exception as e:
#         st.error(f"Error searching files: {str(e)}")
#         return []

# def refresh_index():
#     """Refresh the search index."""
#     try:
#         response = requests.post(f"{API_URL}/refresh")
#         response.raise_for_status()
#         data = response.json()
#         if data["status"] == "ok":
#             return data["result"]
#         return None
#     except Exception as e:
#         st.error(f"Error refreshing index: {str(e)}")
#         return None

# # Set page config
# st.set_page_config(
#     page_title="Google Drive Search",
#     page_icon="🔍",
#     layout="wide"
# )

# # Custom CSS
# st.markdown("""
#     <style>
#     .stButton>button {
#         width: 100%;
#     }
#     .file-list {
#         margin-top: 1rem;
#     }
#     .search-box {
#         margin-bottom: 1rem;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Title and description
# st.title("Search Term RAG")
# st.markdown("""
#     This application allows you to search through your Google Drive files using Search term.
#     You can also view all files and refresh the search index.
# """)

# # Sidebar
# with st.sidebar:
#     st.header("Actions")
    
#     # Refresh index button
#     if st.button("🔄 Refresh Index", help="Update the search index with latest files"):
#         with st.spinner("Refreshing index..."):
#             result = refresh_index()
#             if result:
#                 if result.get('status') == 'success':
#                     st.success(f"✅ Index refreshed successfully!")
#                     st.info(f"Processed {result['files_processed']} files")
#                     if result.get('files_failed', 0) > 0:
#                         st.warning(f"{result['files_failed']} files failed to process.")
#                 else:
#                     st.warning(result.get('message', 'Index refresh completed with warnings.'))
    
#     # Status
#     st.markdown("---")
#     st.subheader("Status")
#     try:
#         response = requests.get(f"{API_URL}/")
#         if response.status_code == 200:
#             st.success("Backend: Connected")
#         else:
#             st.error("Backend: Error")
#     except:
#         st.error("Backend: Not Connected")

# # Main content
# tab1, tab2 = st.tabs(["File List", "Search"])

# with tab1:
#     st.header("Files in Google Drive")
    
#     # Add refresh button
#     if st.button("Refresh File List"):
#         files = list_files()
#     else:
#         files = list_files()
    
#     if files:
#         # Convert to DataFrame
#         df = pd.DataFrame(files)
        
#         # Format dates and file sizes
#         df['created_time'] = df['created_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
#         df['modified_time'] = df['modified_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
#         df['file_size'] = df['file_size'].apply(lambda x: f"{x/1024:.1f} KB" if x < 1024*1024 else f"{x/(1024*1024):.1f} MB")
        
#         # Create markdown link column
#         df['file'] = df.apply(lambda row: f"[{row['file_name']}]({row['file_url']})", axis=1)
        
#         # Drop original columns
#         df = df.drop(['file_url', 'file_id', 'mime_type'], axis=1, errors='ignore')
        
#         # Reorder columns
#         df = df[['file', 'file_extension', 'file_size', 'created_time', 'modified_time']]
        
#         # Rename columns for display
#         df = df.rename(columns={
#             'file': 'File Name',
#             'file_extension': 'Type',
#             'file_size': 'Size',
#             'created_time': 'Created',
#             'modified_time': 'Modified'
#         })
        
#         # Display results
#         st.dataframe(
#             df,
#             column_config={
#                 "File Name": st.column_config.LinkColumn(
#                     "File Name",
#                     help="Click to open file"
#                 ),
#                 "Type": st.column_config.TextColumn(
#                     "Type",
#                     help="File type"
#                 ),
#                 "Size": st.column_config.TextColumn(
#                     "Size",
#                     help="File size"
#                 ),
#                 "Created": st.column_config.TextColumn(
#                     "Created",
#                     help="Creation date"
#                 ),
#                 "Modified": st.column_config.TextColumn(
#                     "Modified",
#                     help="Last modified date"
#                 )
#             },
#             hide_index=True,
#             use_container_width=True
#         )
        
#         # Show file type distribution
#         st.subheader("File Type Distribution")
#         type_counts = df['Type'].value_counts()
#         st.bar_chart(type_counts)
        
#     else:
#         st.info("No files found. Please check your Google Drive folder configuration.")

# with tab2:
#     st.header("Search Files")
    
#     # Add refresh index button
#     if st.button("Refresh Search Index"):
#         result = refresh_index()
#         if result:
#             if result.get('status') == 'success':
#                 st.success(f"Index refreshed successfully. Processed {result['files_processed']} files.")
#                 if result.get('files_failed', 0) > 0:
#                     st.warning(f"{result['files_failed']} files failed to process.")
#             else:
#                 st.warning(result.get('message', 'Index refresh completed with warnings.'))
    
#     # Search functionality
#     search_query = st.text_input("Enter search query", key="search_query")
#     if search_query:
#         results = search_files(search_query)
#         if results:
#             # Convert results to DataFrame
#             df = pd.DataFrame(results)
            
#             # Format dates and file sizes
#             df['created_time'] = df['created_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
#             df['modified_time'] = df['modified_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
#             df['file_size'] = df['file_size'].apply(lambda x: f"{x/1024:.1f} KB" if x < 1024*1024 else f"{x/(1024*1024):.1f} MB")
            
#             # Create markdown link column
#             df['file'] = df.apply(lambda row: f"[{row['file_name']}]({row['file_url']})", axis=1)
            
#             # Drop original columns
#             df = df.drop(['file_url', 'file_id', 'mime_type'], axis=1, errors='ignore')
            
#             # Reorder columns
#             df = df[['file', 'file_extension', 'file_size', 'created_time', 'modified_time', 'score']]
            
#             # Rename columns for display
#             df = df.rename(columns={
#                 'file': 'File Name',
#                 'file_extension': 'Type',
#                 'file_size': 'Size',
#                 'created_time': 'Created',
#                 'modified_time': 'Modified',
#                 'score': 'Relevance Score'
#             })
            
#             # Display results
#             st.dataframe(
#                 df,
#                 column_config={
#                     "File Name": st.column_config.LinkColumn(
#                         "File Name",
#                         help="Click to open file"
#                     ),
#                     "Type": st.column_config.TextColumn(
#                         "Type",
#                         help="File type"
#                     ),
#                     "Size": st.column_config.TextColumn(
#                         "Size",
#                         help="File size"
#                     ),
#                     "Created": st.column_config.TextColumn(
#                         "Created",
#                         help="Creation date"
#                     ),
#                     "Modified": st.column_config.TextColumn(
#                         "Modified",
#                         help="Last modified date"
#                     ),
#                     "Relevance Score": st.column_config.NumberColumn(
#                         "Relevance Score",
#                         help="Search relevance score",
#                         format="%.2f"
#                     )
#                 },
#                 hide_index=True,
#                 use_container_width=True
#             )
            
#             # Display highlights
#             st.subheader("Search Highlights")
#             for result in results:
#                 if 'highlights' in result and result['highlights']:
#                     st.markdown(f"**{result['file_name']}**")
#                     for highlight in result['highlights']:
#                         st.markdown(f"> {highlight}")
#                     st.markdown("---")
#         else:
#             st.info("No results found. Try a different search term or refresh the index.")

# # Footer
# st.markdown("---")
# st.markdown("""
#     <div style='text-align: center'>
#         <p>Google Drive RAG Application | Built with FastAPI, Streamlit, and Elasticsearch</p>
#     </div>
# """, unsafe_allow_html=True) 
'''import streamlit as st
>>>>>>> a1ec42e25924b78808faaef0234f538b0bf9f322
import requests
import json
from datetime import datetime
import pandas as pd
import time
from typing import List, Dict, Any

# Constants
API_URL = "https://web-production-6ef03.up.railway.app/"

def format_file_size(size_bytes):
    """Format file size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def format_date(date_str):
    """Format ISO date string to readable format."""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str

def handle_api_error(e, operation: str):
    """Handle API errors consistently."""
    if isinstance(e, requests.exceptions.ConnectionError):
        st.error(f"Could not connect to the backend server. Please ensure it's running at {API_URL}")
    elif isinstance(e, requests.exceptions.RequestException):
        st.error(f"Error during {operation}: {str(e)}")
    else:
        st.error(f"Unexpected error during {operation}: {str(e)}")

def list_files():
    """List files from Google Drive."""
    try:
        response = requests.get(f"{API_URL}/files")
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            return data["files"]
        return []
    except Exception as e:
        st.error(f"Error listing files: {str(e)}")
        return []

def search_files(query: str):
    """Search for files."""
    try:
        response = requests.get(f"{API_URL}/search", params={"query": query})
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            return data["results"]
        elif data["status"] == "warning":
            st.warning(data["message"])
        return []
    except Exception as e:
        st.error(f"Error searching files: {str(e)}")
        return []

def refresh_index():
    """Refresh the search index."""
    try:
        response = requests.post(f"{API_URL}/refresh")
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            return data["result"]
        return None
    except Exception as e:
        st.error(f"Error refreshing index: {str(e)}")
        return None

# Set page config
st.set_page_config(
    page_title="Google Drive Search",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .file-list {
        margin-top: 1rem;
    }
    .search-box {
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("Search Term RAG")
st.markdown("""
    This application allows you to search through your Google Drive files using Search term.
    You can also view all files and refresh the search index.
""")

# Sidebar
with st.sidebar:
    st.header("Actions")
    
    # Refresh index button
    if st.button("🔄 Refresh Index", help="Update the search index with latest files"):
        with st.spinner("Refreshing index..."):
            result = refresh_index()
            if result:
                if result.get('status') == 'success':
                    st.success(f"✅ Index refreshed successfully!")
                    st.info(f"Processed {result['files_processed']} files")
                    if result.get('files_failed', 0) > 0:
                        st.warning(f"{result['files_failed']} files failed to process.")
                else:
                    st.warning(result.get('message', 'Index refresh completed with warnings.'))
    
    # Status
    st.markdown("---")
    st.subheader("Status")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            st.success("Backend: Connected")
        else:
            st.error("Backend: Error")
    except:
        st.error("Backend: Not Connected")

# Main content
tab1, tab2 = st.tabs(["File List", "Search"])

with tab1:
    st.header("Files in Google Drive")
    
    # Add refresh button
    if st.button("Refresh File List"):
        files = list_files()
    else:
        files = list_files()
    
    if files:
        # Convert to DataFrame
        df = pd.DataFrame(files)
        
        # Format dates and file sizes
        df['created_time'] = df['created_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
        df['modified_time'] = df['modified_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
        df['file_size'] = df['file_size'].apply(lambda x: f"{x/1024:.1f} KB" if x < 1024*1024 else f"{x/(1024*1024):.1f} MB")
        
        # Keep file_name and file_url as separate columns
        df['file_name'] = df['file_name']
        df['file_url'] = df['file_url']
        
        # Drop unnecessary columns
        df = df.drop(['file_id', 'mime_type'], axis=1, errors='ignore')
        
        # Reorder columns
        df = df[['file_name', 'file_url', 'file_extension', 'file_size', 'created_time', 'modified_time']]
        
        # Rename columns for display
        df = df.rename(columns={
            'file_name': 'File Name',
            'file_url': 'URL',
            'file_extension': 'Type',
            'file_size': 'Size',
            'created_time': 'Created',
            'modified_time': 'Modified'
        })
        
        # Display results
        st.dataframe(
            df,
            column_config={
                "File Name": st.column_config.TextColumn(
                    "File Name",
                    help="Name of the file"
                ),
                "URL": st.column_config.LinkColumn(
                    "URL",
                    help="Click to open file"
                ),
                "Type": st.column_config.TextColumn(
                    "Type",
                    help="File type"
                ),
                "Size": st.column_config.TextColumn(
                    "Size",
                    help="File size"
                ),
                "Created": st.column_config.TextColumn(
                    "Created",
                    help="Creation date"
                ),
                "Modified": st.column_config.TextColumn(
                    "Modified",
                    help="Last modified date"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Show file type distribution
        st.subheader("File Type Distribution")
        type_counts = df['Type'].value_counts()
        st.bar_chart(type_counts)
        
    else:
        st.info("No files found. Please check your Google Drive folder configuration.")

with tab2:
    st.header("Search Files")
    
    # Add refresh index button
    if st.button("Refresh Search Index"):
        result = refresh_index()
        if result:
            if result.get('status') == 'success':
                st.success(f"Index refreshed successfully. Processed {result['files_processed']} files.")
                if result.get('files_failed', 0) > 0:
                    st.warning(f"{result['files_failed']} files failed to process.")
            else:
                st.warning(result.get('message', 'Index refresh completed with warnings.'))
    
    # Search functionality
    search_query = st.text_input("Enter search query", key="search_query")
    if search_query:
        results = search_files(search_query)
        if results:
            # Convert results to DataFrame
            df = pd.DataFrame(results)
            
            # Format dates and file sizes
            df['created_time'] = df['created_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
            df['modified_time'] = df['modified_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
            df['file_size'] = df['file_size'].apply(lambda x: f"{x/1024:.1f} KB" if x < 1024*1024 else f"{x/(1024*1024):.1f} MB")
            
            # Keep file_name and file_url as separate columns
            df['file_name'] = df['file_name']
            df['file_url'] = df['file_url']
            
            # Drop unnecessary columns
            df = df.drop(['file_id', 'mime_type'], axis=1, errors='ignore')
            
            # Reorder columns
            df = df[['file_name', 'file_url', 'file_extension', 'file_size', 'created_time', 'modified_time', 'score']]
            
            # Rename columns for display
            df = df.rename(columns={
                'file_name': 'File Name',
                'file_url': 'URL',
                'file_extension': 'Type',
                'file_size': 'Size',
                'created_time': 'Created',
                'modified_time': 'Modified',
                'score': 'Relevance Score'
            })
            
            # Display results
            st.dataframe(
                df,
                column_config={
                    "File Name": st.column_config.TextColumn(
                        "File Name",
                        help="Name of the file"
                    ),
                    "URL": st.column_config.LinkColumn(
                        "URL",
                        help="Click to open file"
                    ),
                    "Type": st.column_config.TextColumn(
                        "Type",
                        help="File type"
                    ),
                    "Size": st.column_config.TextColumn(
                        "Size",
                        help="File size"
                    ),
                    "Created": st.column_config.TextColumn(
                        "Created",
                        help="Creation date"
                    ),
                    "Modified": st.column_config.TextColumn(
                        "Modified",
                        help="Last modified date"
                    ),
                    "Relevance Score": st.column_config.NumberColumn(
                        "Relevance Score",
                        help="Search relevance score",
                        format="%.2f"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Display highlights
            st.subheader("Search Highlights")
            for result in results:
                if 'highlights' in result and result['highlights']:
                    st.markdown(f"**{result['file_name']}**")
                    for highlight in result['highlights']:
                        st.markdown(f"> {highlight}")
                    st.markdown("---")
        else:
            st.info("No results found. Try a different search term or refresh the index.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Google Drive RAG Application | Built with FastAPI, Streamlit, and Elasticsearch</p>
    </div>

""", unsafe_allow_html=True)
=======
""", unsafe_allow_html=True) '''


##new changes to output struct
import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import time
from typing import List, Dict, Any

# Constants
API_URL = "https://web-production-6ef03.up.railway.app/"

def format_file_size(size_bytes):
    """Format file size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def format_date(date_str):
    """Format ISO date string to readable format."""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str

def handle_api_error(e, operation: str):
    """Handle API errors consistently."""
    if isinstance(e, requests.exceptions.ConnectionError):
        st.error(f"Could not connect to the backend server. Please ensure it's running at {API_URL}")
    elif isinstance(e, requests.exceptions.RequestException):
        st.error(f"Error during {operation}: {str(e)}")
    else:
        st.error(f"Unexpected error during {operation}: {str(e)}")

def list_files():
    """List files from Google Drive."""
    try:
        response = requests.get(f"{API_URL}/files")
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            return data["files"]
        return []
    except Exception as e:
        st.error(f"Error listing files: {str(e)}")
        return []

def search_files(query: str):
    """Search for files."""
    try:
        response = requests.get(f"{API_URL}/search", params={"query": query})
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            return data["results"]
        elif data["status"] == "warning":
            st.warning(data["message"])
        return []
    except Exception as e:
        st.error(f"Error searching files: {str(e)}")
        return []

def refresh_index():
    """Refresh the search index."""
    try:
        response = requests.post(f"{API_URL}/refresh")
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            return data["result"]
        return None
    except Exception as e:
        st.error(f"Error refreshing index: {str(e)}")
        return None

# Set page config
st.set_page_config(
    page_title="Google Drive Search",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .file-list {
        margin-top: 1rem;
    }
    .search-box {
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("Search Term RAG")
st.markdown("""
    This application allows you to search through your Google Drive files using Search term.
    You can also view all files and refresh the search index.
""")

# Sidebar
with st.sidebar:
    st.header("Actions")
    
    # Refresh index button
    if st.button("🔄 Refresh Index", help="Update the search index with latest files"):
        with st.spinner("Refreshing index..."):
            result = refresh_index()
            if result:
                if result.get('status') == 'success':
                    st.success(f"✅ Index refreshed successfully!")
                    st.info(f"Processed {result['files_processed']} files")
                    if result.get('files_failed', 0) > 0:
                        st.warning(f"{result['files_failed']} files failed to process.")
                else:
                    st.warning(result.get('message', 'Index refresh completed with warnings.'))
    
    # Status
    st.markdown("---")
    st.subheader("Status")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            st.success("Backend: Connected")
        else:
            st.error("Backend: Error")
    except:
        st.error("Backend: Not Connected")

# Main content
tab1, tab2 = st.tabs(["File List", "Search"])

with tab1:
    st.header("Files in Google Drive")
    
    # Add refresh button
    if st.button("Refresh File List"):
        files = list_files()
    else:
        files = list_files()
    
    if files:
        # Convert to DataFrame
        df = pd.DataFrame(files)
        
        # Format dates and file sizes
        df['created_time'] = df['created_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
        df['modified_time'] = df['modified_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
        df['file_size'] = df['file_size'].apply(lambda x: f"{x/1024:.1f} KB" if x < 1024*1024 else f"{x/(1024*1024):.1f} MB")
        
        # Keep file_name and file_url as separate columns
        df['file_name'] = df['file_name']
        df['file_url'] = df['file_url']
        
        # Drop unnecessary columns
        df = df.drop(['file_id', 'mime_type'], axis=1, errors='ignore')
        
        # Reorder columns
        df = df[['file_name', 'file_url', 'file_extension', 'file_size', 'created_time', 'modified_time']]
        
        # Rename columns for display
        df = df.rename(columns={
            'file_name': 'File Name',
            'file_url': 'URL',
            'file_extension': 'Type',
            'file_size': 'Size',
            'created_time': 'Created',
            'modified_time': 'Modified'
        })
        
        # Display results
        st.dataframe(
            df,
            column_config={
                "File Name": st.column_config.TextColumn(
                    "File Name",
                    help="Name of the file"
                ),
                "URL": st.column_config.LinkColumn(
                    "URL",
                    help="Click to open file"
                ),
                "Type": st.column_config.TextColumn(
                    "Type",
                    help="File type"
                ),
                "Size": st.column_config.TextColumn(
                    "Size",
                    help="File size"
                ),
                "Created": st.column_config.TextColumn(
                    "Created",
                    help="Creation date"
                ),
                "Modified": st.column_config.TextColumn(
                    "Modified",
                    help="Last modified date"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Show file type distribution
        st.subheader("File Type Distribution")
        type_counts = df['Type'].value_counts()
        st.bar_chart(type_counts)
        
    else:
        st.info("No files found. Please check your Google Drive folder configuration.")

with tab2:
    st.header("Search Files")
    
    # Add refresh index button
    if st.button("Refresh Search Index"):
        result = refresh_index()
        if result:
            if result.get('status') == 'success':
                st.success(f"Index refreshed successfully. Processed {result['files_processed']} files.")
                if result.get('files_failed', 0) > 0:
                    st.warning(f"{result['files_failed']} files failed to process.")
            else:
                st.warning(result.get('message', 'Index refresh completed with warnings.'))
    
    # Search functionality
    search_query = st.text_input("Enter search query", key="search_query")
    if search_query:
        results = search_files(search_query)
        if results:
            # Convert results to DataFrame
            df = pd.DataFrame(results)
            
            # Format dates and file sizes
            df['created_time'] = df['created_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
            df['modified_time'] = df['modified_time'].apply(lambda x: x.split('T')[0] if isinstance(x, str) else x)
            df['file_size'] = df['file_size'].apply(lambda x: f"{x/1024:.1f} KB" if x < 1024*1024 else f"{x/(1024*1024):.1f} MB")
            
            # Keep file_name and file_url as separate columns
            df['file_name'] = df['file_name']
            df['file_url'] = df['file_url']
            
            # Drop unnecessary columns
            df = df.drop(['file_id', 'mime_type'], axis=1, errors='ignore')
            
            # Reorder columns
            df = df[['file_name', 'file_url', 'file_extension', 'file_size', 'created_time', 'modified_time', 'score']]
            
            # Rename columns for display
            df = df.rename(columns={
                'file_name': 'File Name',
                'file_url': 'URL',
                'file_extension': 'Type',
                'file_size': 'Size',
                'created_time': 'Created',
                'modified_time': 'Modified',
                'score': 'Relevance Score'
            })
            
            # Display results
            st.dataframe(
                df,
                column_config={
                    "File Name": st.column_config.TextColumn(
                        "File Name",
                        help="Name of the file"
                    ),
                    "URL": st.column_config.LinkColumn(
                        "URL",
                        help="Click to open file"
                    ),
                    "Type": st.column_config.TextColumn(
                        "Type",
                        help="File type"
                    ),
                    "Size": st.column_config.TextColumn(
                        "Size",
                        help="File size"
                    ),
                    "Created": st.column_config.TextColumn(
                        "Created",
                        help="Creation date"
                    ),
                    "Modified": st.column_config.TextColumn(
                        "Modified",
                        help="Last modified date"
                    ),
                    "Relevance Score": st.column_config.NumberColumn(
                        "Relevance Score",
                        help="Search relevance score",
                        format="%.2f"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Display highlights
            st.subheader("Search Highlights")
            for result in results:
                if 'highlights' in result and result['highlights']:
                    st.markdown(f"**{result['file_name']}**")
                    for highlight in result['highlights']:
                        st.markdown(f"> {highlight}")
                    st.markdown("---")
        else:
            st.info("No results found. Try a different search term or refresh the index.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Google Drive RAG Application | Built with FastAPI, Streamlit, and Elasticsearch</p>
    </div>
""", unsafe_allow_html=True)