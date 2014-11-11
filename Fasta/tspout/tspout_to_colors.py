import sys

__author__ = 'krr428'


header = """
<html>
<head>
    <link href='http://fonts.googleapis.com/css?family=Ubuntu+Mono' rel='stylesheet' type='text/css'>
</head>
<body>

<style>
.C {
    background-color: cyan;
}

.G {
    background-color: green;
}

.A {
    background-color: red;
}

.T {
    background-color: yellow;
}

body {
    font-family: 'Ubuntu Mono';
}
</style>
"""

footer = """
</body>
</html>
"""

def read_input_file(filename):
    output = []
    with open(filename) as f:
        for line in f:
            for c in line:
                if c in ['A', 'T', 'C', 'G']:
                    output.append("<span class=" + c + ">" + c + "</span>")
            output.append("<br />\n")
    return "".join(output)

if __name__ == "__main__":
    print header
    print read_input_file(sys.argv[1])
    print footer


