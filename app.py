import io
import json

from flask import Flask, request, render_template, make_response

from utils import extension_validation, process_data_for_output

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def form():
    if request.method == 'POST':
        f = request.files['data_file']
        if not f:
            context = {"error": True, "error_message": "No File"}
        else:
            file_check = extension_validation(f.filename)
            if file_check:
                stream = io.StringIO(f.stream.read().decode("utf-8-sig"), newline=None)
                final_data, error = process_data_for_output(stream)
                if error:
                    context = {"error": True, "error_message": error}
                else:
                    context = {"output": json.dumps(final_data, indent=2), "enable_output": True}
            else:
                context = {"error": True, "error_message": "Incorrect format"}
    else:
        context = dict()
    return render_template("base.html", **context)


@app.route('/sample', methods=["GET"])
def get_sample_json():
    si = io.StringIO()
    try:
        file = open("sample.json", "r").read()
    except Exception as e:
        # just in case when sample.json is not available
        file = '''{"reference":{"ref-temp":50,"ref-hum":50},"data":{"temp-1":{"humidity":[{"timestamp":"2007-04-05T22:12","data":45}],"thermometer":[{"timestamp":"2007-04-05T22:00","data":72.4}]},"temp-2":{"thermometer":[{"timestamp":"2007-04-05T22:12","data":69.4}]}}}'''
    si.write(json.loads(json.dumps(file)))
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=sample.json"
    output.headers["Content-type"] = "text/json"
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
