import argparse
import sys
import os
import subprocess
from pybnafar import Bnafar

def main():
    parser = argparse.ArgumentParser(
        description="🇧🇷 pybnafar CLI - Inteligência Farmacêutica para o SUS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  pybnafar --sync --workspace meu_projeto
  pybnafar --dashboard
  pybnafar --report --ufs MG SP
        """
    )
    
    group = parser.add_argument_group('Operações')
    group.add_argument('--sync', action='store_true', help='Sincroniza snapshots oficiais do OpenDATASUS')
    group.add_argument('--dashboard', action='store_true', help='Inicia o Painel Interativo (Streamlit)')
    group.add_argument('--report', action='store_true', help='Gera relatório de integridade e inteligência no terminal')
    
    config = parser.add_argument_group('Configuração')
    config.add_argument('--workspace', type=str, default='bnafar_system', help='Diretório de trabalho (Data Lake)')
    config.add_argument('--ufs', nargs='+', help='Lista de UFs para filtrar (ex: MG SP)')
    
    args = parser.parse_args()
    
    if args.dashboard:
        dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")
        print(f"🚀 Iniciando Dashboard pybnafar...")
        subprocess.run(["streamlit", "run", dashboard_path, "--", "--workspace", args.workspace])
        return

    bn = Bnafar(workspace=args.workspace)
    
    if args.sync:
        print(f"🔄 Sincronizando dados em: {args.workspace}")
        bn.sync()
    
    if args.report:
        df = bn.load_optimized(ufs=args.ufs)
        if df.empty:
            print("❌ Data Lake vazio ou filtros não retornaram dados.")
            sys.exit(1)
            
        print("\n" + "="*50)
        print("📊 RELATÓRIO DE INTELIGÊNCIA BNAFAR")
        print("="*50)
        
        # Diagnósticos
        bn.diagnostics.check_geographic_bias(df)
        bn.diagnostics.validate_integrity(df)
        
        # Analytics
        rupturas = bn.analytics.detect_real_ruptures(df)
        print(f"\n🚨 Rupturas de Estoque Detectadas: {len(rupturas['confirmed_ruptures'])}")
        if not rupturas['confirmed_ruptures'].empty:
            print(rupturas['confirmed_ruptures'][['sg_uf', 'no_municipio', 'ds_produto']].head())
            
        conf = bn.analytics.calculate_confidence_score(df)
        print(f"\n🛡️ Média do Score de Confiança: {conf['confidence_score'].mean():.2f}")

if __name__ == "__main__":
    main()
