export class AdminComponent {
  empresas = ['Empresa A', 'Empresa B', 'Empresa C'];
  empresaSeleccionada: string = '';
  resultado: any;

  verUsuarios() {
    // Aquí va tu lógica o navegación
    console.log('Mostrar usuarios');
  }

  verAgendamientos() {
    console.log('Mostrar agendamientos de', this.empresaSeleccionada);
  }

  filtrarPorEmpresa() {
    console.log('Filtrar por empresa:', this.empresaSeleccionada);
  }
}
