class DocumentNotFoundError(Exception):
    """
    Veritabanında istenen belge bulunamadığında fırlatılır.
    """
    def __init__(self, message="Belge bulunamadı."):
        super().__init__(message)


class InvalidObjectIdError(Exception):
    """
    Geçersiz bir ObjectId kullanıldığında fırlatılır.
    """
    def __init__(self, message="Geçersiz ObjectId formatı."):
        super().__init__(message)