import json
import logging

import requests

from app import crud, schemas
from app.general.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

interlinkers = [
    {
        "name": "Skeleton to guide the description of the main aim of the collaborative project",
        "nature": "KN",
        "backend": "googledrive",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/knowledge/doc.png",
        "images": [],
        "keywords": "skeleton;aim;project",
        "path": "static/demodata/interlinkers/knowledge/skeleton_to_guide_the_description_of_the_main_aim_of_the_collaborative_project.docx",
    },
    {
        "name": "Collaborative editor",
        "nature": "SW",
        "backend": "etherwrapper",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/etherpad/logo.jpeg",
        "images": ["/static/demodata/interlinkers/etherpad/screenshot.png"],
        "keywords": "collaborative;document;editor;etherpad",
    },
    {
        "name": "File manager",
        "nature": "SW",
        "backend": "filemanager",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/filemanager/logo.png",
        "images": ["/static/demodata/interlinkers/filemanager/screenshot.jpeg"],
        "keywords": "static;file;manager",
    },
    {
        "name": "Forum",
        "nature": "SW",
        "backend": "forum",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/forum/logo.png",
        "images": [],
        "keywords": "forum;chat;conversation;discussion",
    },
    {
        "name": "Google Drive",
        "nature": "SW",
        "backend": "googledrive",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/googledrive/logo.png",
        "images": ["/static/demodata/interlinkers/googledrive/sheets.png", "/static/demodata/interlinkers/googledrive/docs.png", "/static/demodata/interlinkers/googledrive/slides.png"],
        "keywords": "document;share;edit;slide;collaboration",
    }
]


def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    for interlinker in interlinkers:
        nature = interlinker["nature"]
        name = interlinker["name"]
        backend = interlinker["backend"]
        description = interlinker["description"]
        logo = interlinker["logo"]
        keywords = interlinker["keywords"]
        images = interlinker["images"]
        init_asset_id = None

        if crud.interlinker.get_by_name(db=db, name=name):
            return
        try:
            if nature == "KN":
                path = interlinker["path"]
                files_data = {'file': ("demoooo.docx", open(path, "rb"))}
                print(files_data)
                response = requests.post(
                    f"http://{backend}/api/v1/assets/", files=files_data)

                print(f"RESPUESTA PARA {backend}")
                files_data = response.json()
                print(files_data)
                init_asset_id = files_data["_id"]

            print(images)
            # I don´t know why sometimes a tuple that contains InterlinkerVersionCreate instance is created
            crud.interlinker.create(
                db=db,
                interlinker=schemas.InterlinkerCreate(**{
                    "name": name,
                    "description": description,
                    "logotype": logo,
                    "images": images,
                    "published": True,
                    "keywords": keywords,
                    "documentation": """
                        # Dillinger
                        ## _The Last Markdown Editor, Ever_

                        Dillinger is a cloud-enabled, mobile-ready, offline-storage compatible,
                        AngularJS-powered HTML5 Markdown editor.

                        - Type some Markdown on the left
                        - See HTML in the right
                        - ✨Magic ✨

                        ## Features

                        - Import a HTML file and watch it magically convert to Markdown
                        - Drag and drop images (requires your Dropbox account be linked)
                        - Import and save files from GitHub, Dropbox, Google Drive and One Drive
                        - Drag and drop markdown and HTML files into Dillinger
                        - Export documents as Markdown, HTML and PDF

                        Markdown is a lightweight markup language based on the formatting conventions
                        that people naturally use in email.
                        As [John Gruber] writes on the [Markdown site][df1]

                        > The overriding design goal for Markdown's
                        > formatting syntax is to make it as readable
                        > as possible. The idea is that a
                        > Markdown-formatted document should be
                        > publishable as-is, as plain text, without
                        > looking like it's been marked up with tags
                        > or formatting instructions.

                        This text you see here is *actually- written in Markdown! To get a feel
                        for Markdown's syntax, type some text into the left window and
                        watch the results in the right.

                        ## Tech

                        Dillinger uses a number of open source projects to work properly:

                        - [AngularJS] - HTML enhanced for web apps!
                        - [Ace Editor] - awesome web-based text editor
                        - [markdown-it] - Markdown parser done right. Fast and easy to extend.
                        - [Twitter Bootstrap] - great UI boilerplate for modern web apps
                        - [node.js] - evented I/O for the backend
                        - [Express] - fast node.js network app framework [@tjholowaychuk]
                        - [Gulp] - the streaming build system
                        - [Breakdance](https://breakdance.github.io/breakdance/) - HTML
                        to Markdown converter
                        - [jQuery] - duh

                        And of course Dillinger itself is open source with a [public repository][dill]
                        on GitHub.

                        ## Installation

                        Dillinger requires [Node.js](https://nodejs.org/) v10+ to run.

                        Install the dependencies and devDependencies and start the server.

                        ```sh
                        cd dillinger
                        npm i
                        node app
                        ```

                        For production environments...

                        ```sh
                        npm install --production
                        NODE_ENV=production node app
                        ```

                        ## Plugins

                        Dillinger is currently extended with the following plugins.
                        Instructions on how to use them in your own application are linked below.

                        | Plugin | README |
                        | ------ | ------ |
                        | Dropbox | [plugins/dropbox/README.md][PlDb] |
                        | GitHub | [plugins/github/README.md][PlGh] |
                        | Google Drive | [plugins/googledrive/README.md][PlGd] |
                        | OneDrive | [plugins/onedrive/README.md][PlOd] |
                        | Medium | [plugins/medium/README.md][PlMe] |
                        | Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

                        ## Development

                        Want to contribute? Great!

                        Dillinger uses Gulp + Webpack for fast developing.
                        Make a change in your file and instantaneously see your updates!

                        Open your favorite Terminal and run these commands.

                        First Tab:

                        ```sh
                        node app
                        ```

                        Second Tab:

                        ```sh
                        gulp watch
                        ```

                        (optional) Third:

                        ```sh
                        karma test
                        ```

                        #### Building for source

                        For production release:

                        ```sh
                        gulp build --prod
                        ```

                        Generating pre-built zip archives for distribution:

                        ```sh
                        gulp build dist --prod
                        ```

                        ## Docker

                        Dillinger is very easy to install and deploy in a Docker container.

                        By default, the Docker will expose port 8080, so change this within the
                        Dockerfile if necessary. When ready, simply use the Dockerfile to
                        build the image.

                        ```sh
                        cd dillinger
                        docker build -t <youruser>/dillinger:${package.json.version} .
                        ```

                        This will create the dillinger image and pull in the necessary dependencies.
                        Be sure to swap out `${package.json.version}` with the actual
                        version of Dillinger.

                        Once done, run the Docker image and map the port to whatever you wish on
                        your host. In this example, we simply map port 8000 of the host to
                        port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

                        ```sh
                        docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
                        ```

                        > Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

                        Verify the deployment by navigating to your server address in
                        your preferred browser.

                        ```sh
                        127.0.0.1:8000
                        ```

                        ## License

                        MIT

                        **Free Software, Hell Yeah!**

                        [//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

                        [dill]: <https://github.com/joemccann/dillinger>
                        [git-repo-url]: <https://github.com/joemccann/dillinger.git>
                        [john gruber]: <http://daringfireball.net>
                        [df1]: <http://daringfireball.net/projects/markdown/>
                        [markdown-it]: <https://github.com/markdown-it/markdown-it>
                        [Ace Editor]: <http://ace.ajax.org>
                        [node.js]: <http://nodejs.org>
                        [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
                        [jQuery]: <http://jquery.com>
                        [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
                        [express]: <http://expressjs.com>
                        [AngularJS]: <http://angularjs.org>
                        [Gulp]: <http://gulpjs.com>

                        [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
                        [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
                        [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
                        [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
                        [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
                        [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
                    """,
                    "SOC_type": "A11",
                    "nature": nature,
                    "problemdomains": [],
                    "backend": backend,
                    "init_asset_id": init_asset_id
                }
                ),
            )
        except Exception as e:
            print(str(e))
            pass

    db.close()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
