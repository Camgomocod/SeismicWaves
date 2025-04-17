import pandas as pd
import os

def export_validation_results(validation_results, file_path, only_invalid=False):
    """
    Export validation results to CSV
    
    Parameters:
    -----------
    validation_results : list
        List of dictionaries containing validation results
    file_path : str
        Path where to save the CSV file
    only_invalid : bool
        If True, export only invalid results. If False, export all results
    """
    try:
        # Create DataFrame from results
        data = []
        for result in validation_results:
            # Skip valid results if only_invalid is True
            if only_invalid and result['is_valid']:
                continue
                
            details = result['details']
            data.append({
                'File ID': details['file_id'],
                'Is Valid': result['is_valid'],
                'Signal Duration (s)': details['duration'],
                'P Arrival Time (s)': details['relative_p_time'] if details['p_arrival'] else None,
                'Error': result['error'] if not result['is_valid'] else None,
                'Has P Arrival': details.get('has_p_arrival', False)
            })
        
        # Create and save DataFrame
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        
        return True, f"Results exported successfully to {file_path}"
        
    except Exception as e:
        return False, f"Error exporting results: {str(e)}"



def export_example():
    # Create a sample validation result
    validation_result = {
        'is_valid': True,
        'error': None,
        'details': {
            'file_id': 1,
            'duration': 10.5,
            'p_arrival': 2.3,
            'relative_p_time': 2.3,
            'has_p_arrival': True
        }
    }
    
    # Create a list of validation results
    validation_results = [validation_result]
    # Directorio de salida por defecto (home del usuario)
    output_dir = os.path.expanduser("~")
    
    # Exportar todos los resultados
    all_results_path = os.path.join(output_dir, "validation_results_all.csv")
    success, message = export_validation_results(validation_results, all_results_path, only_invalid=False)
    print(message)
    
    # Exportar solo resultados inválidos
    invalid_results_path = os.path.join(output_dir, "validation_results_invalid.csv")
    success, message = export_validation_results(validation_results, invalid_results_path, only_invalid=True)
    print(message)