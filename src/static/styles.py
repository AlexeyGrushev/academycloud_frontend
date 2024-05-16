hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """


set_page_background = """
<style>
.stApp {
    background-image: url('https://i.ibb.co/54jsQN6/background.png');
    background-opacity: 0.3;
    background-size: cover;
    background-position: center;
}
</style>
"""

padding_up_correction = """
<style>
.st-emotion-cache-z5fcl4 {
    width: 100%;
    padding: 0px;
    padding-left: 7%;
    padding-right: 7%;
    padding-bottom: 2%;
    min-width: auto;
    max-width: initial;
}
</style>
"""
