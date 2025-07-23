# EMart Customizations

Comprehensive ERPNext customizations for retail and e-commerce operations covering purchase management, sales, incentives, inventory, billing, PDC management, payments, CRM, reporting, integrations, HRMS, portals, and mobile functionalities.

## Modules

### EMart Purchase Management
- **Purchase Incentive**: Manage supplier incentives and rebates
- Features: Percentage/fixed amount incentives, automatic calculations

### EMart Sales Management  
- **Salesman Target**: Set and track sales targets for salespeople
- Features: Monthly/quarterly/yearly targets, achievement tracking, incentive calculations

### EMart Inventory Management
- **Aging Stock Alert**: Monitor and alert on slow-moving inventory
- Features: Automatic aging calculation, alert levels, recommended actions
- **Damage Tracking**: Track damaged items and write-offs

### EMart CRM
- Customer relationship management enhancements
- Portal integration for customer self-service

### EMart Integrations
- **Integration Settings**: Central configuration for all integrations
- **Barcode Integration**: Barcode scanning for inventory and sales
- **Biometric Integration**: Employee attendance via biometric devices  
- **Tally Integration**: Sync data with Tally ERP
- **WhatsApp Integration**: Customer communication via WhatsApp

### EMart HRMS
- Basic HR management features
- Integration with biometric attendance

### EMart Portals
- **Salesman Portal**: Dashboard for sales personnel
- **Partner Portal**: Self-service portal for business partners

### EMart Reporting
- **Sales Performance Report**: Comprehensive sales analysis
- **Aging Stock Report**: Inventory aging analysis
- Custom dashboards and analytics

### EMart Mobile
- **Mobile Stock Tracking**: Mobile app for stock management
- Features: GPS tracking, barcode scanning, real-time updates

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/mknoufi/emart_customizations --branch develop
bench install-app emart_customizations
```

## Configuration

1. Go to **Integration Settings** to configure:
   - Barcode scanner settings
   - Biometric device connection
   - Tally ERP integration
   - WhatsApp API credentials

2. Set up **Purchase Incentives** for suppliers
3. Create **Salesman Targets** for sales team
4. Configure aging stock thresholds

## Features

### Automated Processes
- Daily aging stock alerts
- Automatic incentive calculations
- Biometric attendance sync
- Tally data synchronization

### Mobile Capabilities
- Mobile stock tracking with GPS
- Barcode scanning
- Real-time inventory updates

### Portal Access
- Salesman dashboard with targets and achievements
- Partner portal for self-service

### Integrations
- Barcode scanning for faster operations
- Biometric attendance tracking
- Tally ERP data sync
- WhatsApp customer communication

## API Endpoints

- `/api/method/emart_customizations.api.get_salesman_dashboard_data`
- `/api/method/emart_customizations.api.scan_barcode`
- `/api/method/emart_customizations.api.send_whatsapp_message`

## Customization

The app is designed to be easily extensible:
- Each module has its own directory structure
- Custom DocTypes follow ERPNext conventions
- Event hooks for automatic processing
- Scheduled tasks for background operations

## License

MIT
