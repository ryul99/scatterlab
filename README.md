[![Build Status](https://travis-ci.com/ryul99/scatterlab.svg?branch=master)](https://travis-ci.com/ryul99/scatterlab)

# to test
`python manage.py test`

# to run dev server
`python manage.py runserver`

# api list

| function (url)                                     | method | 하는 일                         |
|----------------------------------------------------|--------|---------------------------------|
| post (/api/posts/)                                 | GET    | return posts list               |
|                                                    | POST   | make 1 post                     |
| specific_post (/api/posts/<int:post_id>/)          | PUT    | edit 1 post                     |
|                                                    | GET    | return 1 post                   |
|                                                    | DELETE | remove 1 post                   |
| comment (/api/posts/<int:post_id>/comment/)        | POST   | make 1 comment on specific post |
| like_post (/api/posts/<int:post_id>/like/)         | POST   | like to specific post           |
| hate_post (/api/posts/<int:post_id>/hate/)         | POST   | hate to specific post           |
| like_comment (/api/comments/<int:comment_id>/like) | POST   | like to specific comment        |
| hate_comment (/api/comments/<int:comment_id>/hate) | POST   | hate to specific comment        |