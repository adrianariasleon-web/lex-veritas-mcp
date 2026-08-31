from fastmcp import FastMCP
from urllib.parse import urlparse

mcp = FastMCP("LEX-VERITAS")

DOMINIOS_OFICIALES = {
    "scjn.gob.mx": "Suprema Corte de Justicia de la Nación",
    "sjf2.scjn.gob.mx": "Semanario Judicial de la Federación",
    "dof.gob.mx": "Diario Oficial de la Federación",
    "diputados.gob.mx": "Cámara de Diputados",
    "congresosinaloa.gob.mx": "Congreso del Estado de Sinaloa",
}

@mcp.tool
def verificar_fuente_oficial(url: str) -> dict:
   """
    Verifica preliminarmente si una URL pertenece a un dominio jurídico
    oficial autorizado por LEX-VERITAS.
    """
    print("TOOL_CALL verificar_fuente_oficial", flush=True)
    try:
        parsed = urlparse(url)
        dominio = (parsed.hostname or "").lower()

        if dominio.startswith("www."):
            dominio = dominio[4:]

        for dominio_oficial, institucion in DOMINIOS_OFICIALES.items():
            if dominio == dominio_oficial or dominio.endswith("." + dominio_oficial):
                return {
                    "resultado": "FUENTE_OFICIAL_RECONOCIDA",
                    "institucion": institucion,
                    "dominio": dominio,
                    "url": url,
                    "advertencia": (
                        "La pertenencia a un dominio oficial no verifica por sí sola "
                        "la vigencia, aplicabilidad temporal ni fuerza jurídica del contenido."
                    ),
                }

        return {
            "resultado": "FUENTE_NO_RECONOCIDA",
            "dominio": dominio,
            "url": url,
            "advertencia": "Requiere verificación adicional antes de utilizarse como autoridad jurídica.",
        }

    except Exception as e:
        return {
            "resultado": "ERROR_DE_VERIFICACION",
            "detalle": str(e),
        }


@mcp.tool
def estado_lex_veritas() -> dict:
    print("TOOL_CALL estado_lex_veritas", flush=True)
    """Comprueba que el servidor MCP LEX-VERITAS está funcionando."""
    return {
        "sistema": "LEX-VERITAS",
        "estado": "OPERATIVO",
        "version": "0.1.0",
        "modo": "SOLO_LECTURA",
    }


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port
    )
    
