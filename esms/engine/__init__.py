# esms/engine/__init__.py
def init_engine():
    """Initialize engine components like tactics and commentary managers"""
    from esms.engine.tactics import tact_manager
    from esms.engine.commentary import commentary_manager
    import os
    import shutil
    
    # Ensure config files exist
    if not os.path.exists('tactics.dat') and os.path.exists('samples/tactics.dat'):
        shutil.copy('samples/tactics.dat', 'tactics.dat')
    if not os.path.exists('language.dat') and os.path.exists('samples/language.dat'):
        shutil.copy('samples/language.dat', 'language.dat')
    
    # Initialize components
    try:
        tact_manager().init('tactics.dat')
        print("Tactics manager initialized")
    except Exception as e:
        print(f"Warning: Could not initialize tactics manager: {str(e)}")
    
    try:
        commentary_manager().init('language.dat')
        print("Commentary manager initialized")
    except Exception as e:
        print(f"Warning: Could not initialize commentary manager: {str(e)}")