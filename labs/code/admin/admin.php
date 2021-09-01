<html>
    <head>
        <title>Admin Page</title>
    </head>
    <body>
        This is admin page view able only by logged in users.
        <a href="admin.php?_csrf=<?php echo $_SESSION['token']; ?>">dangerous function</>
    </body> 
</html>