def get_html():
    return '''<html> 
    <head>
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
    </style>
    </head>
    <body>
    <div class="site-stats-count">
    [ADD_TABLE]
    </div>
    </body>
    </html>'''
