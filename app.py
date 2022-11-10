from flask import Flask, render_template, request, redirect
import openai


openai.api_key = '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'
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/outline")
def outline():
    return render_template("outline.html")

@app.route("/outline-results")
def outline_results():
    try:
        num = int(request.args.get("number"))
    except:
        return redirect("/outline")
    title = request.args.get("title")

    outline_output = openai.Completion.create(
                    engine='text-davinci-002',
                    prompt="Expand the blog title in to high level blog sections: {} \n\n- Introduction: ".format(title),
                    max_tokens=70,
                    temperature=0.7
                )
    outline_output = outline_output['choices'][0]['text'].splitlines()
    outline_output.insert(0, 'Introduction')
    og_outline_output_len = len(outline_output)
    if og_outline_output_len > num:
        outline_output = outline_output[:num - 1]    
        outline_output.append('Conclusion')
    elif og_outline_output_len < num:
        for x in range(num - og_outline_output_len):
            if num - og_outline_output_len - 1 == x:
                outline_output.append('Conclusion')
            else:
                outline_output.append('')
    filtered_outlines = filtered_outlines = list(filter(lambda el: len(el) > 5, outline_output))
    return render_template('output.html', outline_output=zip(filtered_outlines, range(len(filtered_outlines))), title = title, number=len(filtered_outlines))

@app.route("/paragraphs")
def paragraphing():
    title = request.args.get('title')
    number = request.args.get('number')
    paragraphs = []
    for x in request.args.keys():
        if x not in ['title', 'number']:
            x = request.args.get(x)
            print(x)
            if x != title:
                paragraph = openai.Completion.create(
                            engine='text-davinci-002',
                            prompt=title + '\n\n Continue the following point\n' + x + ":",
                            max_tokens=256,
                            temperature=0.7
                        )['choices'][0]['text']
                if paragraph[-1] == '.':
                    paragraph = paragraph[:-1]
                paragraph = paragraph.lstrip() + '<br /><br />'
            paragraphs.append(paragraph)
    return render_template('full_output.html', paragraphs = paragraphs, title=title)