"""The unit contains a flask_restx parsers to parse data from requests"""
from flask_restx.reqparse import RequestParser
# ------------------------------------------------------------------------

# the parser to get page number for genres and directors
page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int,
                         location='args', required=False)

# the parser to get page and status for movies
movie_parser: RequestParser = RequestParser()
movie_parser.add_argument(name='status', type=str, location='args',
                          required=False)
movie_parser.add_argument(name='page', type=int, location='args',
                          required=False)

# this parser used with favorites views
favorites_parser: RequestParser = RequestParser()
favorites_parser.add_argument(name='Authorization', type=str,
                              location='headers', required=False)
