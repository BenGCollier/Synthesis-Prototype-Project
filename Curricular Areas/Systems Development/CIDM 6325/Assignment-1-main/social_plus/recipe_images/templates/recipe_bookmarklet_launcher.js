(function(){
    if(!window.bookmarklet) {
        recipe_bookmarklet_js = document.body.appendChild(document.createElement('script'));
        recipe_bookmarklet_js.src = '//127.0.0.1:8000/static/js/recipe_bookmarklet.js?r='+Math.floor(Math.random()*9999999999999999);
        window.bookmarklet = true;
    }
    else {
      recipe_bookmarkletLaunch();
    }
  })();