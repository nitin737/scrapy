def get_html():
    return '''<html> 
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <style>
         .site-stats-count{
            text-align: center;

         }

         ul{
             list-style: none;
             display:flex;
         }
         li{
            margin:10px;
            width:130px;
            height:80px;
            border-radius:5px;

            background-image: linear-gradient(rgb(197, 99, 99), rgb(137, 199, 126));
         }

         strong{
            display:block;
             font-weight:bold;
             padding:8px 2px 0px 2px;
             font-size:16pt;
         }

         span{
            display:block;
            padding:2px;
            font-size:13pt;
         }
         table {
            border-collapse: collapse;
            border-spacing: 0;
            width: 100%;
            border: 1px solid #ddd;
         }

         th, td {
            text-align: left;
            padding: 16px;
         }

         tr:nth-child(even) {
            background-color: #f2f2f2;
         }
    </style>
    </head>
    <body>
    <div class="site-stats-count">
    [ADD_TABLE]
    </div>
    </body>
    </html>'''
