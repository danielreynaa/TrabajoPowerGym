import jaydebeapi
import os

class Conexion:
    def __init__(self, host='localhost', database='PowerGym', user='root', password='changeme'):
        self._host = host
        self._database = database
        self._user = user
        self._password = password
        self.conexion = self.createConnection()
        self.conexion.autocommit=False

    def createConnection(self):
        try:
            jdbc_driver = "com.mysql.cj.jdbc.Driver"
            jar_path = os.path.abspath("lib/mysql-connector-j-9.2.0.jar")
            url = f"jdbc:mysql://{self._host}:3306/{self._database}?serverTimezone=UTC"

            conn = jaydebeapi.connect(
                jdbc_driver,
                url,
                [self._user, self._password],
                jar_path
            )
            print("✅ Conexión establecida correctamente.")
            return conn
        except Exception as e:
            print("❌ Error creando conexión:", e)
            return None

    def getCursor(self):
        if self.conexion is None:
            self.conexion = self.createConnection()
        return self.conexion.cursor()

    def closeConnection(self):
        try:
            if self.conexion:
                self.conexion.close()
                self.conexion = None
        except Exception as e:
            print("❌ Error cerrando conexión:", e)

# Prueba (opcional)
# if __name__ == "__main__":
#     Conexion()
