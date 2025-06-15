from flask import Flask, render_template, request

from manager import ResearchAssistant

app = Flask(__name__)


EXAMPLE_PAPERS = {
    "papers": [
        {
            "title": "Exemple de papier 1",
            "authors": "Auteur 1, Auteur 2",
            "abstract": "Ceci est un résumé d'exemple pour le premier papier.",
            "url": "https://example.com/paper1",
        },
        {
            "title": "Exemple de papier 2",
            "authors": "Auteur 3, Auteur 4",
            "abstract": "Ceci est un résumé d'exemple pour le deuxième papier.",
            "url": "https://example.com/paper2",
        },
    ]
}

AGENT = ResearchAssistant()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/install_env", methods=["POST"])
def install_env():
    prompt = request.form.get("prompt")
    #return AGENT.use(prompt)
    return "the result of install_env" 

@app.route("/get_papers", methods=["POST"])
def process():
    prompt = request.form.get("prompt")
    #result = AGENT.use(prompt)
    #return render_template("paper_list.html", papers = result)
    return render_template("paper_list.html", papers=EXAMPLE_PAPERS["papers"])


if __name__ == "__main__":
    app.run(port=1414, debug=True)
