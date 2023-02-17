import sendemail as email

if __name__ == '__main__':
    try:
        email.fnSendEmail(
                'sk_dante@hotmail.com', # Remitente
                ["samuel.rodriguez1292085@gmail.com", "gskdante@gmail.com"], # Destinatarios
                'Correo de Pruebas - Asunto', # Asunto
                '<H1>Hola Mundo</H1>', # Body
                [],   #['prueba.xlsx', 'prueba1.xlsx'], #Ruta de archivos adjuntos
                'sk_dante@hotmail.com', # User
                'SkyAngel7*', # Pwd
                True # Si el body es HTML
                )
    except Exception as e:
        print('---|||||| ERROR: ' + str(e) + ' ||||||---')