from Models.property_placeholder import PropertyPlaceholderDTO


class IPropertyPlaceholderRepository:
    def get_by_id(self, property_id: int) -> PropertyPlaceholderDTO | None:
        pass

    def mark_as_sold(self, property_id: int) -> None:
        pass
