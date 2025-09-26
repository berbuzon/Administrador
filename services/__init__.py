# services/__init__.py

__all__ = ['ReportService', 'generar_reporte_meses']


def __getattr__(name):
    if name == 'ReportService':
        from .report_service import ReportService

        return ReportService
    if name == 'generar_reporte_meses':
        from .report_service_meses import generar_reporte_meses

        return generar_reporte_meses
    raise AttributeError(f"module 'services' has no attribute {name!r}")
