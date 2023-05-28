"""init app"""

from src.main import create_app

app = create_app()

@app.template_filter('get_enum_value')
def get_enum_value(enum_item):
    return enum_item.value


if __name__ == '__main__':
    app.run(debug=True)