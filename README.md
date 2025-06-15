<!-- Centered teaser image -->
<p align="center">
  <img src="res/teaser_unait.png" alt="GitHunter Teaser" width="600"/>
</p>

# GitHunter: Multi-Agent Research Assistant

GitHunter is an intelligent platform for discovering and installing AI repositories based on academic research. The application allows users to easily find, compare, and install reliable AI repositories backed by peer-reviewed research papers.

## Features

- **AI-Powered Discovery**: Our system scans thousands of research papers to find the most relevant repositories
- **Quality Metrics**: Filter by citations, GitHub stars, and recent updates
- **One-Click Installation**: Automatic setup of complex research repositories
- **Modern Interface**: Futuristic design with immersive visual effects (starfield, smooth animations)
- **Dark/Light Mode**: Dark and light theme support for optimal user experience:

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd unaite_def
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**
   
   In the project root, create a file named `.env` and add your Anthropic API key:
   
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Running the Project

Start the server with:
```sh
python server.py
```

After running the command, open the link shown in your terminal (usually `http://127.0.0.1:1414/`) in your web browser. This will open the GitHunter interface.

## Demo

To see the search functionality in action, try entering the following prompt in the search bar:

```
general-purpose method for deep learning on surfaces such as 3D triangle meshes and point clouds like diffusion-net
```

This will list papers related to this topic.

<!-- Centered search result teaser image -->
<p align="center">
  <img src="res/teaser_search.png" alt="Search Result Teaser" width="700"/>
</p>