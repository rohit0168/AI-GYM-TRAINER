
import os
import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# Resolve project paths independently of working directory
BASE_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = BASE_DIR / "static"
CSS_PATH = STATIC_DIR / "style.css"
FONT_PATH = STATIC_DIR / "AdobeClean.otf"


def load_css(file_path=None):
    css_path = Path(file_path) if file_path else CSS_PATH

    if not css_path.is_absolute():
        css_path = BASE_DIR / css_path

    if not css_path.exists():
        st.warning(f"CSS file not found: {css_path}")
        return

    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


def inject_local_font(font_path=None, font_name="AdobeClean"):
    font_path = Path(font_path) if font_path else FONT_PATH

    if not font_path.is_absolute():
        font_path = BASE_DIR / font_path

    if not font_path.exists():
        st.warning(f"Font file not found: {font_path}")
        return

    with open(font_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: '{font_name}';
            src: url('data:font/otf;base64,{encoded}') format('opentype');
            font-weight: 100 900;
            font-style: normal;
            font-display: swap;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def inject_webrtc_styles():
    if not FONT_PATH.exists():
        return

    with open(FONT_PATH, "rb") as font_file:
        encoded_font = base64.b64encode(font_file.read()).decode()

    components.html(
        f"""
        <script>
        (() => {{
            const font = `{encoded_font}`;

            function injectIntoIframe(iframe) {{
                try {{
                    const doc = iframe.contentDocument;
                    if (!doc || !doc.head) return;

                    if (doc.getElementById('webrtc-custom-styles')) return;

                    const style = doc.createElement('style');
                    style.id = 'webrtc-custom-styles';

                    style.textContent = `
                        @font-face {{
                            font-family: 'AdobeClean';
                            src: url('data:font/otf;base64,${{font}}')
                                 format('opentype');
                            font-weight: 100 900;
                            font-style: normal;
                        }}

                        body,
                        button,
                        input,
                        .MuiButtonBase-root,
                        .MuiButton-root {{
                            font-family: 'AdobeClean', sans-serif !important;
                        }}

                        .MuiButtonBase-root,
                        .MuiButton-root {{
                            border-radius: 0 !important;
                        }}
                    `;

                    doc.head.appendChild(style);
                }} catch (e) {{
                    console.warn('WebRTC font injection failed:', e);
                }}
            }}

            function findAndPatch() {{
                document.querySelectorAll('iframe').forEach(iframe => {{
                    if (!iframe.src || !iframe.src.includes('webrtc')) return;

                    if (iframe.contentDocument?.readyState === 'complete') {{
                        injectIntoIframe(iframe);
                    }} else {{
                        iframe.addEventListener(
                            'load',
                            () => injectIntoIframe(iframe),
                            {{ once: true }}
                        );
                    }}
                }});
            }}

            findAndPatch();

            new MutationObserver(findAndPatch).observe(
                document.body,
                {{ childList: true, subtree: true }}
            );
        }})();
        </script>
        """,
        height=0
    )

# import os
# import streamlit as st
# import streamlit.components.v1 as components
# import base64
 

# def load_css(file_path):
#     if os.path.exists(file_path):
#         with open(file_path) as f:
#             st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# def inject_local_font(font_path, font_name):
#     if not os.path.exists(font_path):
#         return
    
#     with open(font_path, "rb") as f:
#         encoded = base64.b64encode(f.read()).decode()

#     ext = os.path.splitext(font_path)[1].lstrip(".")
#     fmt = {"otf": "opentype"}.get(ext, ext)
#     mime = {"otf": "font/otf"}.get(ext, f"font/{ext}")

#     st.markdown(f"""
#         <style>
#         @font-face {{
#             font-family: '{font_name}';
#             src: url('data:{mime};base64,{encoded}') format('{fmt}');
#             font-weight: 100 900;
#             font-style: normal;
#         }}
#         </style>
#     """, unsafe_allow_html=True)

# def inject_webrtc_styles():
#     font_path = os.path.join(os.getcwd(), "static", "AdobeClean.otf")
    
#     if not os.path.exists(font_path):
#         return

#     with open(font_path, "rb") as font_file:
#         encoded_font = base64.b64encode(font_file.read()).decode()

#     components.html(
#         f"""
#         <script>
#         (function patchWebRTCStyles() {{
#             function injectIntoIframe(iframe) {{
#                 try {{
#                     const doc = iframe.contentDocument || iframe.contentWindow.document;
#                     if (!doc || !doc.head) return;
#                     if (doc.head.querySelector('#webrtc-custom-styles')) return;
#                     const style = doc.createElement('style');
#                     style.id = 'webrtc-custom-styles';
#                     style.textContent = `
#                         @font-face {{
#                             font-family: 'AdobeClean';
#                             src: url('data:font/otf;base64,{encoded_font}') format('opentype');
#                             font-weight: 100 900;
#                             font-style: normal;
#                         }}
#                         .MuiButtonBase-root,
#                         .MuiButton-root,
#                         .MuiButton-contained,
#                         .MuiButton-text {{
#                             border-radius: 0 !important;
#                             font-family: 'AdobeClean', sans-serif !important;
#                             letter-spacing: 0.05em !important;
#                         }}
#                     `;
#                     doc.head.appendChild(style);
#                 }} catch (e) {{
#                     console.warn('[patcher] could not inject:', e);
#                 }}
#             }}

#             function findAndPatch() {{
#                 const parentDoc = window.parent.document;
#                 const iframes = parentDoc.querySelectorAll('iframe');
#                 iframes.forEach(iframe => {{
#                     if (iframe.src && iframe.src.includes('webrtc')) {{
#                         if (iframe.contentDocument && iframe.contentDocument.readyState === 'complete') {{
#                             injectIntoIframe(iframe);
#                         }} else {{
#                             iframe.addEventListener('load', () => injectIntoIframe(iframe));
#                         }}
#                     }}
#                 }});
#             }}

#             findAndPatch();
#         }})();
        </script>
        """,
        height=0,
    )
