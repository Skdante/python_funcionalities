import smtplib
import email.message
import os 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

'''
    function:           fnLoadCFGJSON
    param<strFilepath>: ruta del archivo json    
    description:        lee un archivo JSON 
    return:             diccionario apartir de un JSON
'''
def fnSendEmail(remitente_req, destinatarios_req, asunto_req, body_req, adjuntos, user_req, password_req, is_html):
    try:
        # Iniciamos los parámetros del script
        remitente = remitente_req
        destinatarios = destinatarios_req
        asunto = asunto_req
        cuerpo = str(body_req)

        # Creamos el objeto mensaje
        mensaje = MIMEMultipart('alternative')
            
        # Establecemos los atributos del mensaje
        mensaje['From'] = remitente
        mensaje['To'] = ", ".join(destinatarios)
        mensaje['Subject'] = asunto
            
        # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
        if is_html:
            mensaje.attach(MIMEText(cuerpo, 'html'))
        else:
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            
        for f in adjuntos:
            # Abrimos el archivo que vamos a adjuntar
            archivo_adjunto = open(f, 'rb')    
            # Creamos un objeto MIME base
            adjunto_MIME = MIMEBase('application', 'octet-stream')
            # Y le cargamos el archivo adjunto
            adjunto_MIME.set_payload((archivo_adjunto).read())
            # Codificamos el objeto en BASE64
            encoders.encode_base64(adjunto_MIME)
            # Agregamos una cabecera al objeto
            adjunto_MIME.add_header('Content-Disposition', "attachment; filename= {0}".format(os.path.basename(f)))
            # Y finalmente lo agregamos al mensaje
            mensaje.attach(adjunto_MIME)
            
        # Creamos la conexión con el servidor
        # sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        sesion_smtp = smtplib.SMTP('smtp.live.com', 25)
            
        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        sesion_smtp.login(user_req, password_req)

        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)
        # Cerramos la conexión
        sesion_smtp.quit()
    except Exception as e:
        print("---|||||| ERROR: Send Email {0} ||||||---".format(e))
        print(traceback.format_exc())
        print(sys.exc_info()[0])
    return True