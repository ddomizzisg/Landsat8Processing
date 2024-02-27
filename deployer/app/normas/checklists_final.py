"""
    sources: cadenas de texto representativas de donde se buscaran los datos
"""
SOURCE_API_CONTAINERS = "API_CONTAINERS"
SOURCE_CFG_FILE = "CFG_FILE"
SOURCES = [SOURCE_API_CONTAINERS, SOURCE_CFG_FILE]

"""
    keywords: palabras clave que indican o dan indicio de que se cumple o se realiza cierto proceso
"""
KEYWORD_CPABE = "CP-ABE"
KEYWORD_CPABE_POLITICS = "CP-ABE POLITICS"
KEYWORD_MICROSERVICE_USER_AUTHENTICATION = "AUTHENTICATION MICROSERVICE"

KEYWORD_PRIVATEK_CRYPT = "AES"
KEYWORD_PUBLICK_CRYPT = "RSA"
KEYWORD_SHA3 = "SHA3"
KEYWORD_MD5 = "MD5"
KEYWORD_BLOCKCHAIN = "BLOCKCHAIN"
KEYWORD_DUPLICITY = "DEDUPLICATION"
KEYWORD_IDA = "IDA"

KEYWORD_MICROSERVICE_METADATA = "METADATA MICROSERVICE"
KEYWORD_PUB_SUB = "PUB/SUB"
KEYWORD_BALANCED = "BALANCING"
KEYWORD_CONTAINERS = "CONTAINERS"
KEYWORD_MICROSERVICES = "MICROSERVICES"
KEYWORD_PORTS_SECURITY = "PORTS_SECURITY"
KEYWORD_HTTPS = "HTTPS"
KEYWORD_AUDIT = "AUDIT"
KEYWORD_EVENT_LOG = "LOG"
KEYWORD_AUDIT_REPORTS = "REPORTS"
KEYWORD_DATA_ANONYMIZATION_INR = "INR ANONYNIMIZATION";
KEYWORD_CDN = "CDN"
KEYWORD_NETWORK_CONTROL_NFRS = "NETWORK CONTROL NFRS"

"""
    Checklists como diccionarios de datos
"""

ISO = {
    "name": "ISO 27001-13",
    "requirements": [
        {
            "category": "Gestión de activos",
            "concept": "Propiedad de los activos",
            "keywords": [KEYWORD_CPABE],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Gestión de activos",
            "concept": "Devolución de activos",
            "keywords": [KEYWORD_CPABE],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Requisitos de negocio para el control de accesos",
            "keywords": [KEYWORD_CPABE],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Política de control de accesos",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Control de acceso a las redes y servicios asociados",
            "keywords": [KEYWORD_CPABE],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Gestión de información confidencial de autenticación de usuarios",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Responsabilidades del usuario",
            "keywords": [],
            "assisted": True,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Uso de información confidencial para autenticación",
            "keywords": [KEYWORD_CPABE],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Restricción del acceso a la información",
            "keywords": [KEYWORD_CPABE],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Procedimientos seguros de inicio de sesión",
            "keywords": [KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de acceso",
            "concept": "Gestión de contraseñas de usuario",
            "keywords": [KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad en la operativa",
            "concept": "Gestión de cambios",
            "keywords": [KEYWORD_BLOCKCHAIN, KEYWORD_EVENT_LOG], ##El gestor de logs no lo hace? los hash, la metadata?
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad en la operativa",
            "concept": "Protección de los registros de información",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT, KEYWORD_CPABE],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad en las telecomunicaciones",
            "concept": "Gestión de la seguridad en las redes",
            "keywords": [],
            "assisted": True,
            "compliance": False
        },
        {
            "category": "Seguridad en las telecomunicaciones",
            "concept": "Controles de red",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS, KEYWORD_NETWORK_CONTROL_NFRS],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad en las telecomunicaciones",
            "concept": "Mecanismos de seguridad asociados a servicios en red",
            "keywords": [],
            "assisted": True, #??
            "compliance": False
        },
        {
            "category": "Seguridad en las telecomunicaciones",
            "concept": "Segregación de redes",
            "keywords": [],
            "assisted": True, #??
            "compliance": False
        },
        {
            "category": "Aspectos de seguridad de la información en la gestión de la continuidad del negocio",
            "concept": "Planificación de la continuidad de la seguridad de la información",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Aspectos de seguridad de la información en la gestión de la continuidad del negocio",
            "concept": "Implantación de la continuidad de la seguridad de la información",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_CPABE, KEYWORD_PUBLICK_CRYPT],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Aspectos de seguridad de la información en la gestión de la continuidad del negocio",
            "concept": "Redundancias",
            "keywords": [KEYWORD_DUPLICITY],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Aspectos de seguridad de la información en la gestión de la continuidad del negocio",
            "concept": "Disponibilidad de instalaciones para el procesamiento de la información",
            "keywords": [KEYWORD_DUPLICITY],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Cumplimiento",
            "concept": "Protección de los registros de la organización",
            "keywords": [KEYWORD_CPABE, KEYWORD_IDA],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Cumplimiento",
            "concept": "Protección de datos y privacidad de la información personal",
            "keywords": [
                KEYWORD_PRIVATEK_CRYPT,
                KEYWORD_PUBLICK_CRYPT,
                KEYWORD_SHA3, 
                KEYWORD_MD5,
                KEYWORD_IDA,
            ],
            "assisted": False,
            "compliance": False
        },
    ],
}

#-------------------------------------------
NIST = {
    "name": "NIST",
    "requirements": [
        {
            "category": "Gestión de identidad, autenticación y control de acceso (PR.AC)",
            "concept": "Se gestiona el acceso remoto",
            "keywords": [KEYWORD_CPABE, KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Gestión de identidad, autenticación y control de acceso (PR.AC)",
            "concept": "Se gestionan los permisos y autorizaciones de acceso con incorporación de los principios de menor privilegio y separación de funciones",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS, KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Gestión de identidad, autenticación y control de acceso (PR.AC)",
            "concept": "Las identidades son verificadas y vinculadas a credenciales y afirmadas en las interacciones",
            "keywords": [KEYWORD_CPABE, KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Gestión de identidad, autenticación y control de acceso (PR.AC)",
            "concept": "Se autentican los usuarios, dispositivos y otros activos (por ejemplo, autenticación de un solo factor o múltiples factores) acorde al riesgo de la transacción (por ejemplo, riesgos de seguridad y privacidad de individuos y otros riesgos para las organizaciones)",
            "keywords": [KEYWORD_CPABE, KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad de los datos (PR.DS)",
            "concept": "Los datos en reposo están protegidos",
            "keywords": [
                KEYWORD_IDA,
                KEYWORD_CPABE,
                KEYWORD_PRIVATEK_CRYPT,
                KEYWORD_PUBLICK_CRYPT,
            ],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad de los datos (PR.DS)",
            "concept": "Los datos en tránsito están protegidos",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad de los datos (PR.DS)",
            "concept": "Los activos se gestionan formalmente durante la eliminación, las transferencias y la disposición",
            "keywords": [KEYWORD_MICROSERVICE_METADATA, KEYWORD_PUB_SUB],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad de los datos (PR.DS)",
            "concept": "Se mantiene una capacidad adecuada para asegurar la disponibilidad",
            "keywords": [KEYWORD_DUPLICITY, KEYWORD_IDA],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad de los datos (PR.DS)",
            "concept": "Se implementan protecciones contra las filtraciones de datos",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT, KEYWORD_IDA],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad de los datos (PR.DS)",
            "concept": "Se utilizan mecanismos de comprobación de la integridad para verificar el software, el firmware y la integridad de la información",
            "keywords": [KEYWORD_SHA3, KEYWORD_MD5, KEYWORD_BLOCKCHAIN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Seguridad de los datos (PR.DS)",
            "concept": "Los entornos de desarrollo y prueba(s) están separados del entorno de producción",
            "keywords": [KEYWORD_CONTAINERS, KEYWORD_MICROSERVICES], #??
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Procesos y procedimientos de protección de la información (PR.IP)",
            "concept": "Los datos son eliminados de acuerdo con políticas",
            "keywords": [], #???????
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Procesos y procedimientos de protección de la información (PR.IP)",
            "concept": "Se mejoran los procesos de protección",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT],
            "assisted": False,
            "compliance": False
        },
           {
            "category": "Tecnología de protección (PR.PT)",
            "concept": " Las redes de comunicaciones y control están protegidas",
            "keywords": [],
            "assisted": True, #?
            "compliance": False
        },
        {
            "category": "Tecnología de protección (PR.PT)",
            "concept": "Se implementan mecanismos (por ejemplo, a prueba de fallas, equilibrio de carga, cambio en caliente o “hot swap”) para lograr los requisitos de resiliencia en situaciones normales y adversas",
            "keywords": [KEYWORD_DUPLICITY, KEYWORD_BALANCED, KEYWORD_IDA],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Monitoreo Continuo de la  Seguridad (DE.CM)",
            "concept": "Se monitorea la red para detectar posibles eventos de seguridad cibernética",
            "keywords": [],
            "assisted": True, #?
            "compliance": False
        },
        {
            "category": "Monitoreo Continuo de la  Seguridad (DE.CM)",
            "concept": " Se monitorea el entorno físico para detectar posibles eventos de seguridad cibernética",
            "keywords": [],
            "assisted": True, #?
            "compliance": False
        },
        {
            "category": "Comunicaciones (RS.CO)",
            "concept": "La información se comparte de acuerdo con los planes de respuesta",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT, KEYWORD_IDA],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Comunicaciones (RS.CO)",
            "concept": "El intercambio voluntario de información se produce con las partes interesadas externas para lograr una mayor conciencia situacional de seguridad cibernética",
            "keywords": [
                KEYWORD_PRIVATEK_CRYPT,
                KEYWORD_PUBLICK_CRYPT,
                KEYWORD_CPABE, 
                KEYWORD_SHA3, 
                KEYWORD_MD5,
                KEYWORD_PUB_SUB,
            ],
            "assisted": False,
            "compliance": False
        },
    ],
}


COBIT = {
    "name": "COBIT 5",
    "requirements": [
        {
            "category": "Entrega de servicios requeridos, desde operaciones tradicionales hasta el entrenamiento, pasando seguridad y continuidad. Incluye procesamiento de los datos por sistemas de aplicación.",
            "concept": "Garantizar la Seguridad de Sistemas: El objetivo es salvaguardar la información contra usos no autorizados, divulgación, modificación, daño o pérdida, realizando controles de acceso lógico que aseguren que el acceso a sistemas, datos y programas está restringido a usuarios autorizados",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT, KEYWORD_CPABE],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Entrega de servicios requeridos, desde operaciones tradicionales hasta el entrenamiento, pasando seguridad y continuidad. Incluye procesamiento de los datos por sistemas de aplicación.",
            "concept": "Administrar la Configuración: El objetivo es dar cuenta de todos los componentes de TI, prevenir alteraciones no autorizadas, verificar la existencia física y proporcionar una base para el sano manejo de cambios realizando controles que identifiquen y registren todos los activos de TI así como su localización física y un programa regular de verificación que confirme su existencia",
            "keywords": [KEYWORD_SHA3, KEYWORD_MD5, KEYWORD_BLOCKCHAIN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Entrega de servicios requeridos, desde operaciones tradicionales hasta el entrenamiento, pasando seguridad y continuidad. Incluye procesamiento de los datos por sistemas de aplicación.",
            "concept": "Administrar Datos: El objetivo es asegurar que los datos permanezcan completos, precisos y válidos durante su entrada, actualización, salida y almacenamiento, a través de una combinación efectiva de controles generales y de aplicación sobre las operaciones de TI",
            "keywords": [
                KEYWORD_PRIVATEK_CRYPT,
                KEYWORD_PUBLICK_CRYPT,
                KEYWORD_SHA3, 
                KEYWORD_MD5,
                KEYWORD_IDA,
            ],
            "assisted": False,
            "compliance": False
        },
    ],
}


MEX = {
    "name": "Norma Oficial Mexicana NOM-024-SSA3-2010",
    "requirements": [
        {
            "category": "Autenticación",
            "concept": "Debe establecer un número máximo de 3 autenticaciones no exitosas para bloquear la cuenta.",
            "keywords": [KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Autenticación",
            "concept": "Debe autenticar a los usuarios, organizaciones, dispositivos u objetos antes de permitir el acceso a la información.",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS, KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Autenticación",
            "concept": "Debe denegar el acceso y uso de la información del sistema de los Registros Electrónicos de Salud, y la infraestructura que lo soporta, a todos los usuarios, organizaciones, dispositivos u objetos no autorizados, implementando mecanismos de seguridad que garanticen la integridad y confidencialidad de la información.",
            "keywords": [KEYWORD_CPABE, KEYWORD_SHA3, KEYWORD_MD5, KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Autenticación",
            "concept": " Debe autenticar a los usuarios, organizaciones, dispositivos u objetos, usando al menos uno de los siguientes mecanismos de autenticación: nombre del usuario y contraseña, certificado digital o datos biométricos.",
            "keywords": [KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Autorización de entidades",
            "concept": "Debe administrar los permisos de control de acceso a la información y a los programas informáticos concedidos a usuarios, organizaciones, instituciones, dispositivos y/o aplicaciones informáticas",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Autorización de entidades",
            "concept": "Debe incluir mecanismos informáticos de seguridad del sistema de expediente con la capacidad de conceder autorizaciones a usuarios, organizaciones, instituciones, dispositivos y/o aplicaciones informáticas",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Control de Acceso",
            "concept": "Debe mantener controles de acceso a nivel de módulos, subsistemas, expedientes, formatos y campos para cada rol de usuario",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Control de Acceso",
            "concept": "Debe utilizar listas de control de acceso.",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de Acceso",
            "concept": "Debe contar con interfaces de usuario restringidas basadas en roles",
            "keywords": [KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de Acceso",
            "concept": "Debe utilizar alguna forma de cifrado en sus comunicaciones",
            "keywords": [KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de Acceso",
            "concept": "Debe contar con protección de puertos de dispositivos y el bloqueo de todos aquellos puertos que no tengan una justificación de uso, tanto en TCP como en UDP",
            "keywords": [KEYWORD_PORTS_SECURITY],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Control de Acceso",
            "concept": "Debe contar con una autenticación centralizada adicional a la que se tenga a nivel de equipo de cómputo",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Control de Acceso",
            "concept": "Debe configurar y aplicar reglas de control de acceso al sistema y a los datos, a nivel de componente, aplicación y usuario, para las organizaciones, dispositivos, objetos y usuarios",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS, KEYWORD_MICROSERVICE_USER_AUTHENTICATION], #Cifrado
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Intercambio seguro de datos",
            "concept": " Debe comunicar y transmitir datos de manera cifrada.",
            "keywords": [KEYWORD_PUBLICK_CRYPT, KEYWORD_PRIVATEK_CRYPT],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Intercambio seguro de datos",
            "concept": " Debe incorporar al menos un algoritmo de cifrado simétrico y al menos dos longitudes de llave -una de ellas de al menos 128 bits y la otra de longitud superior-, a ser utilizados para cifrar los archivos electrónicos que contienen datos personales antes de su transmisión. Asimismo, deberá incorporar un mecanismo que permita al remitente enviar al destinatario de forma segura la llave de cifrado utilizada. Estos elementos deberán ser usados cuando los sistemas de expedientes clínicos electrónicos se encuentren en ubicaciones físicas diferentes y/o cuando el intercambio sea entre instituciones u organizaciones tanto públicas como privadas",
            "keywords": [KEYWORD_PUBLICK_CRYPT, KEYWORD_PRIVATEK_CRYPT], #especificar > 128 bits?
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Intercambio seguro de datos",
            "concept": "Debe, en el caso de la transmisión de datos al interior de la unidad médica utilizar medios seguros de comunicación como puede ser el uso del protocolo HTTPS.",
            "keywords": [KEYWORD_HTTPS],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Intercambio seguro de datos",
            "concept": "Debe cifrar en todo evento de comunicación al menos, los datos del paciente",
            "keywords": [KEYWORD_PUBLICK_CRYPT, KEYWORD_PRIVATEK_CRYPT],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Intercambio seguro de datos",
            "concept": " Debe utilizar algoritmos y protocolos basados en normas y estándares internacionales para el cifrado de datos para su transmisión.",
            "keywords": [KEYWORD_PUBLICK_CRYPT, KEYWORD_PRIVATEK_CRYPT, KEYWORD_SHA3, KEYWORD_MD5],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Ruteo Seguro de la Información entre entidades autorizadas",
            "concept": "Debe asegurar que la transmisión de información se realice desde y hacia entidades autorizadas, en tiempo y forma, y sobre medios de transmisión seguros",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS, KEYWORD_PRIVATEK_CRYPT, KEYWORD_PUBLICK_CRYPT, KEYWORD_SHA3, KEYWORD_MD5],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Ruteo Seguro de la Información entre entidades autorizadas",
            "concept": " Debe mantener actualizadas las listas de entidades autorizadas para el envío y recepción de datos",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Ratificación de la información",
            "concept": "Debe ratificar la autoría de la información que es capturada en cada evento del sistema",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS], #podría asumirse este requerimiento si se utiliza CP ABE?
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Ratificación de la información",
            "concept": "Debe permitir el reconocimiento de datos ratificados por usuarios u organizaciones diferentes del autor, correctamente identificados y autorizados",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS], #igual que el requerimiento anterior
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Ratificación de la información",
            "concept": "  Se recomienda utilizar mecanismos de identificación electrónica como el medio para la ratificación de contenidos",
            "keywords": [KEYWORD_CPABE, KEYWORD_CPABE_POLITICS], #¿es correcto?
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Confidencialidad y privacidad del paciente",
            "concept": "Debe mantener la confidencialidad de la información",
            "keywords": [KEYWORD_PUBLICK_CRYPT, KEYWORD_PRIVATEK_CRYPT],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Confidencialidad y privacidad del paciente",
            "concept": "Debe disociar los datos del paciente para fines de estadística e investigación de conformidad con la Ley de Información Estadística y Geográfica",
            "keywords": [KEYWORD_DATA_ANONYMIZATION_INR],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Rastros de auditoría",
            "concept": "Debe poder configurar los eventos que serán registrados en el rastro de auditoría",
            "keywords": [KEYWORD_BLOCKCHAIN],
            "assisted": False, 
            "compliance": False
        },

        {
            "category": "Rastros de auditoría",
            "concept": "Debe registrar los intentos y accesos a los recursos del sistema, incluyendo el registro del usuario, recurso involucrado, la actividad realizada o intentada, y el momento (hora y fecha)",
            "keywords": [KEYWORD_MICROSERVICE_USER_AUTHENTICATION],
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Rastros de auditoría",
            "concept": " Debe registrar quién (usuarios, organizaciones, dispositivos u objetos) y cuándo se ha creado, actualizado, traducido, visto, extraído y/o eliminado un expediente o elemento del mismo",
            "keywords": [KEYWORD_EVENT_LOG], #esto dependería del sistema de distribución de contenido?
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Rastros de auditoría",
            "concept": "Debe mantener una bitácora de la información intercambiada entre sistemas registrando el motivo por el cuál se realiza la transmisión, cuándo ocurre (fecha y hora), identificación del origen y del destino, información intercambiada",
            "keywords": [KEYWORD_CDN, KEYWORD_EVENT_LOG], ##HGRA no sería tambien el Log?
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Rastros de auditoría",
            "concept": "Debe generar reportes configurables de los rastros de auditoría del sistema",
            "keywords": [KEYWORD_AUDIT_REPORTS], #esto se podría verificar con la Blockchain? 
            "assisted": False,
            "compliance": False
        },

        {
            "category": "Rastros de auditoría",
            "concept": "Debe mantener la integridad de los registros de auditoría.",
            "keywords": [KEYWORD_BLOCKCHAIN], 
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Rastros de auditoría",
            "concept": "Debe controlar el uso de y el acceso a los registros de auditoría conforme a la normatividad aplicable y las políticas institucionales u organizacionales",
            "keywords": [KEYWORD_BLOCKCHAIN],
            "assisted": False,
            "compliance": False
        },
        
        {
            "category": "Sincronización",
            "concept": "Debe sincronizar la información con el índice nacional de pacientes que para tal fin ponga a su disposición la Secretaría de Salud a través de los medios y mecanismos establecidos por esta última.",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Sincronización",
            "concept": "Debe sincronizarse en un plazo máximo de 24 horas a partir de la captura de nuevos datos.",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Sincronización",
            "concept": "Debe sincronizar sólo la información de pacientes que tengan completos sus datos de identificación.",
            "keywords": [KEYWORD_CDN], 
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Sincronización",
            "concept": "Debe apegarse a los mecanismos y estructura de mensajería electrónica que para tal fin publique la Secretaría de Salud",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Consultas de información del expediente clínico electrónico",
            "concept": "Debe permitir consultar datos con fines estadísticos al personal cuyo rol lo requiera",
            "keywords": [KEYWORD_CDN, KEYWORD_CPABE, KEYWORD_CPABE_POLITICS], ##HGRA por los roles no se usa también CP-ABE o el de autenticación
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Consultas de información del expediente clínico electrónico",
            "concept": "Debe generar conjuntos de datos identificados, para emitir reportes para fines de investigación",
            "keywords": [KEYWORD_CDN, KEYWORD_CPABE, KEYWORD_CPABE_POLITICS], ##HGRA por los roles no se usa también CP-ABE o el de autenticación
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Consultas de información del expediente clínico electrónico",
            "concept": "Debe generar una serie completa de datos que constituyen el registro de salud de un individuo dentro del sistema",
            "keywords": [KEYWORD_CDN], #HGRA son claros o anonimizados 
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Consultas de información del expediente clínico electrónico",
            "concept": "Se recomienda poder generar un reporte de datos con fines administrativos",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Consultas de información del expediente clínico electrónico",
            "concept": "Se recomienda poder generar un reporte con fines financieros.",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Consultas de información del expediente clínico electrónico",
            "concept": "Se recomienda poder generar reportes con fines de análisis de calidad",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Consultas de información del expediente clínico electrónico",
            "concept": "Se recomienda poder generar un reporte con fines de salud pública",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Interoperabilidad de los Sistemas Estatales, Nacionales e Institucionales",
            "concept": "Debe apegarse a los protocolos definidos para interactuar con Sistemas Estatales, Institucionales o Nacionales de interoperabilidad de acuerdo a los lineamientos que para este fin sean publicados por la Secretaría de Salud",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        },
        {
            "category": "Interoperabilidad de los Sistemas Estatales, Nacionales e Institucionales",
            "concept": "Debe apegarse a los protocolos definidos para los servicios de registros",
            "keywords": [KEYWORD_CDN],
            "assisted": False,
            "compliance": False
        }
        
    ],
}
