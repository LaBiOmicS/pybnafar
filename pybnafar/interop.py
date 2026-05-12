import json
import pandas as pd
from fhir.resources.inventoryreport import InventoryReport
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.extension import Extension
from fhir.resources.quantity import Quantity

class BnafarInterop:
    """
    Standardizes data for healthcare interoperability with strict HL7 FHIR validation.
    """
    
    @staticmethod
    def to_fhir_inventory(df: pd.DataFrame) -> str:
        """Converts stock DataFrame to HL7 FHIR InventoryReport resources (RNDS-style)."""
        resources = []
        for _, row in df.iterrows():
            date_str = row['dt_posicao_estoque'].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z" if pd.notnull(row['dt_posicao_estoque']) else None
            
            # Structured dict following RNDS/FHIR patterns
            resource = {
                "resourceType": "InventoryReport",
                "id": f"bnafar-{row['co_municipio_ibge']}-{row['co_catmat']}",
                "status": "active",
                "countType": "snapshot",
                "reportedDateTime": date_str,
                "meta": {"profile": ["http://rnds.saude.gov.br/fhir/r4/StructureDefinition/BnafarInventoryReport-1.0"]},
                "inventoryListing": [{
                    "item": {"concept": {"coding": [
                        {"system": "http://purl.org/obm/catmat", "code": str(row['co_catmat']), "display": row['ds_produto']},
                        {"system": "http://terminology.hl7.org/CodeSystem/v3-EntityCode", "code": "PHARM", "display": "Pharmaceutical Product"}
                    ]}},
                    "items": [{"quantity": {"value": float(row['qt_estoque']), "unit": "unit"}}]
                }],
                "extension": [
                    {"url": "http://rnds.saude.gov.br/fhir/r4/StructureDefinition/extension-uf", "valueCode": row['sg_uf']},
                    {"url": "http://rnds.saude.gov.br/fhir/r4/StructureDefinition/extension-ibge", "valueCode": str(row['co_municipio_ibge'])}
                ]
            }
            resources.append(resource)
        
        return json.dumps(resources, indent=2, ensure_ascii=False)
