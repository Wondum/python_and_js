document.addEventListener('DOMContentLoaded', function() {
  
  list_articles(page_type);
  
});

function list_articles() {

  fetch(`/get_articles/${page_type}/${article_id}`)
  .then(response => 
    {
      if (!response.ok) { throw response }
        return response.json()
    })
  .then(articles => {
    console.clear();
    
    const article_container = document.createElement('div');
    const article_row = document.createElement('div');
    const article_title_div = document.createElement('div')
    const article_title_h = document.createElement('h1')
    const article_br = document.createElement('br')
    
    article_row.classList="row"
    articles['data'].forEach(content => {
      //Display each post
      console.log(articles);
      display_article(article_row, content)
    })

    article_container.classList="container"
    article_title_h.textContent=articles['mag'].title
    article_title_h.style.fontSize="80px"
    article_title_div.style.textAlign="center"
    article_title_div.style.fontFamily="Brush Script MT"
    article_title_div.appendChild(article_title_h)
    article_container.appendChild(article_title_div)
    article_container.appendChild(article_br)
    article_container.appendChild(article_row)
    
    // preview_article.html
    document.querySelector('#magazine-div').append(article_container);
    //Display pagination bar at the bottom
    //display_nav_bar(articles['total_page_count'])
    
  })
  .catch( err => {
    console.log(err);
  });

}


function display_article(article_row, article){
  const article_col = document.createElement('div');
  const article_col_title = document.createElement('div');
  const article_col_content = document.createElement('div');
  const article_col_pic = document.createElement('div');
  
  const article_hr_div = document.createElement('div');
  const article_hr = document.createElement('hr');
  const article_by = document.createElement('p');

  article_col.style.columnCount= article["article_column"]
  article_col.style.pageBreakAfterr="always"

  article_col_title.style.fontWeight = "bold"
  article_col_title.style.fontFamily="Candara"
  article_col_title.style.fontSize="40px"
  article_col_title.textContent=article["title"]

  article_by.textContent= "by " + article["article_by"]
  article_by.style.fontFamily="Garamond, serif;"
  article_by.style.fontStyle="italic"

  if (article["article_picture"] != "") {
    const article_col_article_pic = document.createElement('embed');
    article_col_article_pic.id="image_style"
    article_col_article_pic.type="image/jpg"
    article_col_article_pic.src=article["article_picture"]
    article_col_pic.appendChild(article_col_article_pic)
  }
  
  article_col_content.textContent=article["content"]
  
  
  article_hr.id="hr_style"
  article_hr_div.appendChild(article_hr)

  article_col.appendChild(article_col_title)
  article_col.appendChild(article_by)
  if (article["article_picture"] != "") {
    article_col.appendChild(article_col_pic)
  }
  
  article_col.appendChild(article_col_content)
  
  article_row.appendChild(article_col)
  article_row.appendChild(article_hr_div)
}

