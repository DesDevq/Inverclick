# property_placeholder.py
#
# ATENCION: esta tabla NO es la tabla definitiva de Propiedades (CA2).
# Es un modelo minimo (solo id + status) creado unicamente para poder
# programar y probar Leads y Ventas (CA3) mientras tu companera termina
# la tabla real de Propiedades.
#
# Cuando ella la tenga lista, hay que hacer 2 cambios (y ya):
#   1. Cambiar el ForeignKey en Models/lead.py y Models/sale.py de
#      "properties_placeholder.id" a la tabla real (ej. "properties.id").
#   2. Borrar este archivo y la tabla "properties_placeholder" de Docker.
from sqlalchemy import String, Integer, Identity
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base


class PropertyStatus:
    """Valores posibles para el campo 'status' de una propiedad."""
    LISTED = "listed"   # publicada en el catalogo, se puede vender
    SOLD = "sold"        # ya vendida, no se puede volver a vender ni listar
    DRAFT = "draft"      # registrada pero aun no publicada en el catalogo


class PropertyPlaceholderDTO(Base):
    __tablename__ = "properties_placeholder"

    id: Mapped[int] = mapped_column(Integer, Identity(
        always=False, start=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=PropertyStatus.LISTED)
