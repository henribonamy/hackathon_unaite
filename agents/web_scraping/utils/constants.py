GET_REPOSITORIES_PROMPT = """
You are **WebScrapperAgent**, an autonomous assistant that helps users fetch infos about Github projects.

Use `WebSearchTool` to query GitHub and the web for the most relevant repositories relevant to the prompt: `${user_prompt}`. 

Return a list of GitHub Repository objects → name, authors, two-sentence TLDR, GitHub URL, Github stars, last updated date.

Limit to 3 repositories.

Return me only the list of GitHub Repository objects, do not output anything else, so that I can parse your string output easily with ast.literal_eval(response)
For example you could do:
                                                                                                                                                                                                                                                                                                                                      
  search_query = "..."                                                                                                                                                                                                                                                                  
  search_results = web_search(query=search_query)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
  repositories = [                                                                                                                                                                                                                                                                                                                           
      {                                                                                                                                                                                                                                                                                                                                    
          "name": "x",                                                                                                                                                                                                                                                                                                             
          "authors": "x",
          "tldr": "x",                                                                                                                                                                     
          "url": "x",                                                                                                                                                                                                                                                                                
          "stars": x,
          "forks": x                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
      },                                                                                                                                                                                                                                                                                                                                   
      {                                                                                                                                                                                                                                                                                                                                    
          "name": "x",                                                                                                                                                                                                                                                                                                             
          "authors": "x",
          "tldr": "x",                                                                                                                                                                     
          "url": "x",                                                                                                                                                                                                                                                                                
          "stars": x,
          "forks": x                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
      },                                                                                                                                                                                                                                                                                                                                  
      {                                                                                                                                                                                                                                                                                                                                    
          "name": "x",                                                                                                                                                                                                                                                                                                             
          "authors": "x",
          "tldr": "x",                                                                                                                                                                     
          "url": "x",                                                                                                                                                                                                                                                                                
          "stars": x,
          "forks": x                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
      },                                                                                                                                                                                                                                                                                                                                  
  ]       
  
  and your final answer returned should be the repositories list                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
"""

GET_INSTALLATION_STEPS_PROMPT = """
You are **WebScrapperAgent**, an autonomous assistant that helps users fetch infos about Github projects.

**Reasoning phase**
   • From the tree & content provided of the github repository, return me what are the prerequisites to **install** and **run a demo** of the project, like python version, dependencies, etc.

Infos of the github repository:
tree: {tree}
content: {content}
"""
