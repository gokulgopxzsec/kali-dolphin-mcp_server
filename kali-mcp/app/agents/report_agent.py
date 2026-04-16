from datetime import datetime


def generate_report(target, recon_results, nuclei_results, rag_results):
    safe_target = target.replace('.', '_').replace('/', '_')
    report_path = f'app/reports/{safe_target}_report.md'

    content = f'''# Security Report for {target}

Generated: {datetime.now()}

## Recon Results
{recon_results}

## Nuclei Results
{nuclei_results}

## RAG Correlation
{rag_results}
'''

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return report_path
