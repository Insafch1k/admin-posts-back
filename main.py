from application.api import app

from domain.keywords.dal import KeywordDAL


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)