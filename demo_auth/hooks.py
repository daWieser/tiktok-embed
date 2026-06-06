import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Create demo user after module installation"""
    _logger.info("Creating demo user...")
    
    # Check if demo user already exists
    existing_user = env['res.users'].search([('login', '=', 'demo')], limit=1)
    
    if existing_user:
        _logger.info(f"Demo user already exists (ID: {existing_user.id}), updating password...")
        existing_user.write({'password': 'demo'})
    else:
        # Create demo user
        try:
            demo_user = env['res.users'].create({
                'name': 'Demo User',
                'login': 'demo',
                'password': 'demo',
            })
            _logger.info(f"Demo user created successfully (ID: {demo_user.id})")
        except Exception as e:
            _logger.error(f"Failed to create demo user: {e}")
