SELECTION_XMLIDS = (
    ("field_property_type_selection_apartment", "field_property_type", "Appartment"),
    ("field_property_type_selection_house", "field_property_type", "House"),
    ("field_property_type_selection_studio", "field_property_type", "Studio"),
    ("field_property_type_selection_office", "field_property_type", "Office"),
    (
        "field_property_type_selection_commercial_space",
        "field_property_type",
        "Commercial space",
    ),
    ("field_property_type_selection_warehouse", "field_property_type", "Warehouse"),
    ("field_property_type_selection_land", "field_property_type", "Land"),
    ("field_property_type_selection_garage", "field_property_type", "Garage"),
    ("field_property_type_selection_room", "field_property_type", "Room"),
    (
        "field_property_invoice_status_selection_no",
        "field_property_invoice_status",
        "no",
    ),
    (
        "field_property_invoice_status_selection_invoiced",
        "field_property_invoice_status",
        "invoiced",
    ),
    (
        "field_property_invoice_status_selection_to_invoice",
        "field_property_invoice_status",
        "to_invoice",
    ),
)


def migrate(cr, version):
    """Restore XML IDs lost from the property-type selection rows.

    Without these IDs, an upgrade treats the existing rows as new records and
    fails on the unique constraint for (field_id, value).
    """
    for xmlid, field_xmlid, value in SELECTION_XMLIDS:
        cr.execute(
            """
            INSERT INTO ir_model_data (module, name, model, res_id, noupdate)
            SELECT
                'industry_real_estate',
                %s,
                'ir.model.fields.selection',
                selection.id,
                FALSE
            FROM ir_model_fields_selection AS selection
            JOIN ir_model_data AS field_xmlid
                ON field_xmlid.model = 'ir.model.fields'
               AND field_xmlid.res_id = selection.field_id
               AND field_xmlid.module = 'industry_real_estate'
               AND field_xmlid.name = %s
            WHERE selection.value = %s
              AND NOT EXISTS (
                  SELECT 1
                  FROM ir_model_data AS selection_xmlid
                  WHERE selection_xmlid.module = 'industry_real_estate'
                    AND selection_xmlid.name = %s
              )
            """,
            (xmlid, field_xmlid, value, xmlid),
        )
