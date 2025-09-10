from dotenv import load_dotenv
import os

class Config:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        # Eğer daha önce initialize edilmişse tekrar yapma
        if Config._initialized:
            return
            
        # ---! .env dosyasını yükle
        self._load_env_file()
        self.postgres_host = self._get_postgres_host()
        self.postgres_port = self._get_postgres_port()
        self.postgres_user = self._get_postgres_user()
        self.postgres_password = self._get_postgres_password()
        self.postgres_database = self._get_postgres_database()
        
        # Search API Service configuration
        self.search_api_host = self._get_search_api_host()
        self.search_api_port = self._get_search_api_port()
        
        Config._initialized = True
        
    def _load_env_file(self) -> None:
        env_path = os.getenv("ENV_PATH")
        if env_path:
            load_dotenv(env_path)
        elif os.path.exists(".env.example"):
            load_dotenv(".env.example")
        elif os.path.exists(".env"):
            load_dotenv(".env")
        else:
            raise FileNotFoundError("🔧 Debug: .env veya .env.example dosyası bulunamadı")
            
    def _get_postgres_host(self) -> str:
        """Entra redirect uri bilgisini environment variable'dan al"""
        postgres_host = os.getenv("POSTGRES_HOST", "default-host")
        if not postgres_host or postgres_host == "default-host":
            raise ValueError("POSTGRES_HOST environment variable bulunmadı")
        return postgres_host
    
    def _get_postgres_port(self) -> str:
        """Postgres port bilgisini environment variable'dan al"""
        postgres_port = os.getenv("POSTGRES_PORT", "default-port")
        if not postgres_port or postgres_port == "default-port":
            raise ValueError("POSTGRES_PORT environment variable bulunmadı")
        return postgres_port
        
    def _get_postgres_database(self) -> str:
        """Postgres database bilgisini environment variable'dan al"""
        postgres_database = os.getenv("POSTGRES_DATABASE", "default-database")
        if not postgres_database or postgres_database == "default-database":
            raise ValueError("POSTGRES_DATABASE environment variable bulunmadı")
        return postgres_database
    
    def _get_postgres_user(self) -> str:
        """Postgres user bilgisini environment variable'dan al"""
        postgres_user = os.getenv("POSTGRES_USER", "default-user")
        if not postgres_user or postgres_user == "default-user":
            raise ValueError("POSTGRES_USER environment variable bulunmadı")
        return postgres_user
    
    def _get_postgres_password(self) -> str:
        """Postgres password bilgisini environment variable'dan al"""
        postgres_password = os.getenv("POSTGRES_PASSWORD", "default-password")
        if not postgres_password or postgres_password == "default-password":
            raise ValueError("POSTGRES_PASSWORD environment variable bulunmadı")
        return postgres_password
    
    def _get_search_api_host(self) -> str:
        """Search API service host bilgisini environment variable'dan al"""
        search_api_host = os.getenv("SEARCH_API_HOST", "localhost")
        return search_api_host
    
    def _get_search_api_port(self) -> int:
        """Search API service port bilgisini environment variable'dan al"""
        search_api_port = os.getenv("SEARCH_API_PORT", "8083")
        return int(search_api_port)

    
    def validate_config(self) -> bool:
        """Konfigürasyon değerlerini doğrula"""
        try:            
            if not self.postgres_host:
                return False
            if not self.postgres_port:
                return False
            if not self.postgres_user:
                return False
            if not self.postgres_password:
                return False
            if not self.postgres_database:
                return False
            if not self.search_api_host:
                return False
            return True
        except Exception:
            return False