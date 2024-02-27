import mysql.connector

db = mysql.connector.connect(
  host = "mysql-db",
  user = "root",
  password = "secret",
  port = 3306,
  database = "scheme_info",
  auth_plugin='mysql_native_password'
)
mycursor = db.cursor(buffered=True)

def insert_containers(id_container,id_long,name,status,image,volumes,entrypoint,platform,description,docker_port,host_port,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p):
  sql = "INSERT INTO containers (id_container,id_long,name,status,image,volumes,entrypoint,platform,description,docker_port,host_port,td_scheme_pub,td_scheme_priv,image_p,volumes_p,status_p) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (id_container,id_long,name,status,image,volumes,entrypoint,platform,description,docker_port,host_port,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p)
  mycursor.execute(sql,val)
  db.commit()

def insert_containers_utility(id_container,id_long,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp,utility_p):
  sql = "INSERT INTO containers_utility (id_container,id_long,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp_utility,utility_p) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (id_container,id_long,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp,utility_p)
  mycursor.execute(sql,val)
  db.commit()

def insert_app(name,description,containers,td_schema):
  sql = "INSERT INTO applications (name,description,td_scheme) VALUES (%s,%s,%s)"
  td_schema = str(td_schema)
  print(td_schema)
  val = (name,description,td_schema)
  mycursor.execute(sql,val)
  db.commit()

  sql = "SELECT id_app FROM applications WHERE name = %s"
  val = (name, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  id_app = res[0]
  for i in range(0,len(containers)):
    insert_app_containers(id_app,containers[i])

def insert_app_containers(id_app,id_container):
  sql = "INSERT INTO applications_containers (id_app,id_container) VALUES (%s,%s)"
  val = (id_app,id_container)
  mycursor.execute(sql,val)
  db.commit()

def insert_app_structure(name_app,structure_json,status_json):
  sql = "INSERT INTO applications_graph (name_app,structure_json,status_json) VALUES (%s,%s,%s)"
  val = (name_app,structure_json,status_json)
  mycursor.execute(sql,val)
  db.commit()

def insert_actions(name,uri,id_container):
  sql = "INSERT INTO actions (name,URI) VALUES (%s,%s)"
  val = (name,uri)
  mycursor.execute(sql,val)
  db.commit()
  sql = "SELECT id_action FROM actions ORDER BY id_action DESC LIMIT 1"
  mycursor.execute(sql)
  res = mycursor.fetchone()
  id_action = res[0]
  sql = "INSERT INTO containers_actions (id_container,id_action) VALUES (%s,%s)"
  val = (id_container,id_action)
  mycursor.execute(sql,val)
  db.commit()

def insert_containers_extras(name_container,type,extra,URI):
  sql = "INSERT INTO containers_extras (name_container,type,extra,URI) VALUES (%s,%s,%s,%s)"
  val = (name_container,type,extra,URI)
  mycursor.execute(sql,val)
  db.commit()

def select_container_tdSchema(id_container):
  sql = "SELECT td_scheme_pub FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  td_schema = res[0]
  return td_schema

def select_container_info(id_container):
  sql = "SELECT name,status,image,volumes,platform,description FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchall()
  info = res[0]
  name = info[0]
  status = info[1]
  image = info[2]
  volumes = info[3]
  platform = info[4]
  description = info[5]
  return name,status,image,volumes,platform,description

def select_container_name(id_container):
  sql = "SELECT name FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  name = res[0]
  return name

def select_container_status(id_container):
  sql = "SELECT status FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  status = res[0]
  return status

def select_container_image(id_container):
  sql = "SELECT image FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  image = res[0]
  return image

def select_container_volumes(id_container):
  sql = "SELECT volumes FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  volumes = res[0]
  return volumes

def select_container_platform(id_container):
  sql = "SELECT platform FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  platform = res[0]
  return platform

def select_container_description(id_container):
  sql = "SELECT description FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  description = res[0]
  return description


#print(select_container_tdSchema("e35bea536b4b"))