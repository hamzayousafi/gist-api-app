from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests

def process_json(gistname):
  html_temp = """"""

  response = requests.get('https://api.github.com/users/'+gistname+'/gists')
  res_json = response.json().copy()

  if isinstance(res_json,dict):
    html_temp+=f"""<div class="result-heading-container">
              <p class="result-heading">USER NOT FOUND :(</p>
              </div>
              """
    return html_temp

  else:
    len_res = len(res_json)

    html_temp+=f"""<div class="result-heading-container">
                <p class="result-heading">{len_res} RESULTS FOUND for <span style="color:red;">"{gistname}"</span>:</p>
                </div>
              """

    for k,i in enumerate(res_json):
      html_temp+=f"""
                <div class="data-box-outer">
                <div class="data-box-inner">
                  
                  <div style="min-height: 3px;"></div>

                  <p class="gist-heading">Gist {k+1}</p>
                """
    
      html_temp+=f"""
                <div class="gist-files">
                  <p class="gist-file-heading"><span style="margin-left:8px;">Gist's Files</span></p>
                  <ul>
                """
      if len(i['files'].items())>0:
        c = 1
        for j in i['files'].items():
          html_temp+=f"""
          <li>
            <div class="filetype-des">
              <div>
                <i class="fa fa-file" aria-hidden="true"></i>
                <span class="file-name">File Link: <a class="file-link" href="{j[1]["raw_url"]}" target="_blank">{j[1]["filename"]}</a></span>
              </div>
              <span class="file-type">File Type: {j[1]["type"]}</span>
              <span>
            </div>
          </li>
          """
          c+=1
      else:
        html_temp+=f"""
        <li>
          <span class="file-name">NO FILES FOUND</span>
        </li>
          """

      html_temp+=f"""
                </ul>
                </div>
                
                <div class="gist-forks">
                  <p class="gist-fork-heading"><span style="margin-left:8px;">Gist's Latest Forks</span></p>
                  <ul>
                """

      fork_url = i['forks_url']
      fork_res = requests.get(fork_url)
      fork_res_json = fork_res.json().copy()
      lat_3_forks = fork_res_json[-3:]

      if len(lat_3_forks) > 0:
        fc=1
        for fork in lat_3_forks:
          html_temp+=f"""
                    <li>
                      <img src="{fork['owner']["avatar_url"]}" class="fork-avatar">
                      <span class="fork-name"><a class="file-link" href="{fork['owner']['html_url']}" target="_blank">{fork['owner']['login']}</a></span>
                    </li>
                    """
          fc+=1
      else:
        html_temp+=f"""
                  <li>
                    <span class="fork-name">Gist Never Forked</span>
                  </li>
                  """

      html_temp+=f"""
                </ul>
                </div>

                <div style="height:10px;visibility: hidden;"></div>
                
                </div>
                </div>
                """
    
    return html_temp

  return html_temp


@csrf_exempt
def get_api_view(request):

  html_start = f"""
            <!DOCTYPE html>
            <html lang="en" >
            <head>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <meta name="author" content="Hamza Tariq">
              <title>GIST APP</title>
              <link rel="shortcut icon" href="{settings.STATIC_URL}GitHub-Mark-Light-32px.png" type="image/x-icon">
              <link href="https://fonts.googleapis.com/css?family=Poppins:400,600,700&display=swap" rel="stylesheet">
              <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
              <script src="https://kit.fontawesome.com/f0601b0fb2.js" crossorigin="anonymous"></script>
              <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css"/>
              
              <link rel="stylesheet" href="{settings.STATIC_URL}new.css">

            </head>
            <body>

            <div class="container-m">
              
                <div class="form-box">

                  <div class="">
                    <div class="" style="margin-top:50px;margin-bottom:50px;">
                      <div class="chip">
                        <div class="chip-icon"><i class="fa fa-github" aria-hidden="true"></i></div>
                        <p>GIST API APP</p>
                      </div>
                    </div>
                  </div>

                  <form method='POST'>
                    <div class="search">
                      <input type="text" name="gistuser" class="search-input" placeholder="Search..." required autofocus>
                      <div class="search-icon"><i class="fa fa-search" aria-hidden="true"></i></div>
                    </div>
                  </form>

                </div>

            </div>

            """


  html_main = f""""""


  html_end = """
            </body>
            </html>
            """

  if request.method != 'POST':
    html_main=''
    return HttpResponse(html_start+html_main+html_end)
  elif request.POST["gistuser"].strip() == '':
    print(request.POST.items())
    html_main=''
    return HttpResponse(html_start+html_main+html_end)
  else:
    html_main=process_json(request.POST["gistuser"].strip())
    return HttpResponse(html_start+html_main+html_end)

  return HttpResponse(html_start+html_main+html_end)