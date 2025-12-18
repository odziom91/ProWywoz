#
# ProWywóz
# v.0.3.0
#

import gi
import sys
import requests
import json
import os
import logging

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk

class Corimp_api():
    # this is class with all API calls for Corimp webpage
    def __init__(self):
        # init api base url
        self.api = 'https://server5.ichisystem.eu/corimp'
        self.city_id = None

    def dl_streets(self):
        # download all streets for Bydgoszcz
        # get Bydgoszcz city ID
        cities = '/addresses/cities'
        r_cities = requests.get(f'{self.api}{cities}')
        r_json_cities = json.loads(r_cities.text)
        for entry in r_json_cities:
            if entry['value'] == 'BYDGOSZCZ':
                self.city_id = entry['id']
        # get streets for Bydgoszcz city ID
        streets = f'/addresses/streets/{self.city_id}'
        r_streets = requests.get(f'{self.api}{streets}')
        r_json_streets = json.loads(r_streets.text)
        return r_json_streets
    
    def dl_buildings(self, street_id):
        # download all buildings on the selected street
        buildings = '/addresses/numbers'
        r_buildings = requests.get(f'{self.api}{buildings}/{self.city_id}/{street_id}')
        r_json_buildings = json.loads(r_buildings.text)
        return r_json_buildings
    
    def save_pdf(self, dialog, result, point_id):
        # get report and download PDF file
        try:
            pdf = '/reports'
            r_pdf = requests.get(f'{self.api}{pdf}?type=pdf&id={point_id}')
            r_pdf.raise_for_status()
            r_json_pdf = json.loads(r_pdf.text)
            url = r_json_pdf['filePath']
            r_download = requests.get(f'{url}')
            file = dialog.save_finish(result)
            path = file.get_path()
            logging.info('Saving to the file...')
            with open(path, 'wb') as f:
                f.write(r_download.content)
            self.info_dialog('Pobieranie harmonogramu PDF', 'Plik z harmonogramem wywozu odpadów został pobrany pomyślnie.')
        except requests.exceptions.ConnectionError as e:
            self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. API nieprawidłowe.\nJeśli problem będzie się potwarzał zgłoś błąd.')
        except requests.exceptions.HTTPError as e:
            logging.error(f'Cannot load streets. {str(e)}')
            if r_pdf.status_code == 403:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Dostęp zabroniony.\nJeśli problem będzie się powtarzał zgłoś błąd.')
            if r_pdf.status_code == 404:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Nieprawidłowy endpoint do API.\nJeśli problem będzie się powtarzał zgłoś błąd.')
            if r_pdf.status_code == 500:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Błąd serwera - spróbuj później.')
            if r_pdf.status_code == 502:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Błąd bramy - spróbuj później.')
            if r_pdf.status_code == 503:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Usługa niedostępna - spróbuj później.')
        except Exception as e:
            logging.error(f'Cannot load streets. Unknown error. {str(e)}')
            raise Exception(f'Nie można pobrać pliku PDF. Nieznany błąd. {str(e)}')


    def error_dialog(self, t, b):
        # error dialog
        err = Gtk.AlertDialog(
            buttons=['OK']
            )
        err.set_message(t)
        err.set_detail(b)
        err.show()

    def info_dialog(self, t, b):
        # info dialog
        ifo = Gtk.AlertDialog(
            buttons=['OK']
        )
        ifo.set_message(t)
        ifo.set_detail(b)
        ifo.show()

class ProNatura_api():
    # this is class with all API calls for ProNatura webpage
    def __init__(self):
        # init api base url
        self.api = 'https://zs5cv4ng75.execute-api.eu-central-1.amazonaws.com'

    def dl_streets(self):
        # download all streets
        try:
            streets = '/prod/streets'
            logging.info('Downloading streets...')
            r_streets = requests.get(f'{self.api}{streets}')
            r_streets.raise_for_status()
            r_json = json.loads(r_streets.text)
            return r_json
        except requests.exceptions.ConnectionError as e:
            raise requests.exceptions.ConnectionError(f'Nie można pobrać ulic. API nieprawidłowe.\nJeśli problem będzie się potwarzał zgłoś błąd.')
        except requests.exceptions.HTTPError as e:
            logging.error(f'Cannot load streets. {str(e)}')
            if r_streets.status_code == 403:
                raise requests.exceptions.HTTPError(f'Nie można pobrać ulic. Dostęp zabroniony.\nJeśli problem będzie się powtarzał zgłoś błąd.')
            if r_streets.status_code == 404:
                raise requests.exceptions.HTTPError(f'Nie można pobrać ulic. Nieprawidłowy endpoint do API.\nJeśli problem będzie się powtarzał zgłoś błąd.')
            if r_streets.status_code == 500:
                raise requests.exceptions.HTTPError(f'Nie można pobrać ulic. Błąd serwera - spróbuj później.')
            if r_streets.status_code == 502:
                raise requests.exceptions.HTTPError(f'Nie można pobrać ulic. Błąd bramy - spróbuj później.')
            if r_streets.status_code == 503:
                raise requests.exceptions.HTTPError(f'Nie można pobrać ulic. Usługa niedostępna - spróbuj później.')
        except Exception as e:
            logging.error(f'Cannot load streets. Unknown error. {str(e)}')
            raise Exception(f'Nie można pobrać ulic. Nieznany błąd. {str(e)}')
    
    def dl_buildings(self, id):
        # download all buildings on the selected street
        try:
            address_points = '/prod/address-points'
            logging.info('Downloading buildings on the street...')
            r_address_points = requests.get(f'{self.api}{address_points}/{id}')
            r_address_points.raise_for_status()
            r_json = json.loads(r_address_points.text)
            return r_json
        except requests.exceptions.ConnectionError as e:
            raise requests.exceptions.ConnectionError(f'Nie można pobrać numerów budynków. API nieprawidłowe.\nJeśli problem będzie się potwarzał zgłoś błąd.')
        except requests.exceptions.HTTPError as e:
            logging.error(f'Cannot load streets. {str(e)}')
            if r_address_points.status_code == 403:
                raise requests.exceptions.HTTPError(f'Nie można pobrać numerów budynków. Dostęp zabroniony.\nJeśli problem będzie się powtarzał zgłoś błąd.')
            if r_address_points.status_code == 404:
                raise requests.exceptions.HTTPError(f'Nie można pobrać numerów budynków. Nieprawidłowy endpoint do API.\nJeśli problem będzie się powtarzał zgłoś błąd.')
            if r_address_points.status_code == 500:
                raise requests.exceptions.HTTPError(f'Nie można pobrać numerów budynków. Błąd serwera - spróbuj później.')
            if r_address_points.status_code == 502:
                raise requests.exceptions.HTTPError(f'Nie można pobrać numerów budynków. Błąd bramy - spróbuj później.')
            if r_address_points.status_code == 503:
                raise requests.exceptions.HTTPError(f'Nie można pobrać numerów budynków. Usługa niedostępna - spróbuj później.')
        except Exception as e:
            logging.error(f'Cannot load streets. Unknown error. {str(e)}')
            raise Exception(f'Nie można pobrać numerów budynków. Nieznany błąd. {str(e)}')

    def save_pdf(self, dialog, result, id):
        # prepare pdf for selected point
        try:
            pdf = '/prod/trash-schedule'
            logging.info('Generating url for download pdf file...')
            r_pdf = requests.get(f'{self.api}{pdf}/{id}/pdf')
            r_pdf.raise_for_status()
            r_json = json.loads(r_pdf.text)
            r_url = r_json['url']
            logging.info('Downloading pdf file...')
            r_download = requests.get(f'{r_url}')
            r_pdf.raise_for_status()
            file = dialog.save_finish(result)
            path = file.get_path()
            logging.info('Saving to the file...')
            with open(path, 'wb') as f:
                f.write(r_download.content)
            self.info_dialog('Pobieranie harmonogramu PDF', 'Plik z harmonogramem wywozu odpadów został pobrany pomyślnie.')
        except requests.exceptions.ConnectionError as e:
            self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. API nieprawidłowe.\nJeśli problem będzie się potwarzał zgłoś błąd.')
        except requests.exceptions.HTTPError as e:
            logging.error(f'Cannot load streets. {str(e)}')
            if r_pdf.status_code == 403 or r_download.status_code == 403:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Dostęp zabroniony.\nJeśli problem będzie się powtarzał zgłoś błąd.')
            if r_pdf.status_code == 404 or r_download.status_code == 404:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Nieprawidłowy endpoint do API.\nJeśli problem będzie się powtarzał zgłoś błąd.')
            if r_pdf.status_code == 500 or r_download.status_code == 500:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Błąd serwera - spróbuj później.')
            if r_pdf.status_code == 502 or r_download.status_code == 502:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Błąd bramy - spróbuj później.')
            if r_pdf.status_code == 503 or r_download.status_code == 503:
                self.error_dialog('Błąd', f'Nie można pobrać pliku PDF. Usługa niedostępna - spróbuj później.')
        except Exception as e:
            logging.error(f'Cannot load streets. Unknown error. {str(e)}')
            raise Exception(f'Nie można pobrać pliku PDF. Nieznany błąd. {str(e)}')
        
    def error_dialog(self, t, b):
        # error dialog
        err = Gtk.AlertDialog(
            buttons=['OK']
            )
        err.set_message(t)
        err.set_detail(b)
        err.show()

    def info_dialog(self, t, b):
        # info dialog
        ifo = Gtk.AlertDialog(
            buttons=['OK']
        )
        ifo.set_message(t)
        ifo.set_detail(b)
        ifo.show()
    
class ProWywoz(Adw.Application):
    def __init__(self):
        try:
            # about app
            self.app_name = 'ProWywóz'
            self.app_version = '0.3.0'
            self.app_icon = os.path.join(os.path.dirname(__file__), "gfx")
            self.app_icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
            self.app_icon_theme.add_search_path(self.app_icon)
            self.app_comments = 'Aplikacja do generowania harmonogramu odbioru odpadów w Bydgoszczy.\n' \
                'Program obsługuje poniższe wyszukiwarki:\n' \
                '- usługa świadczona przez MKUO ProNatura \nSp. z o.o. w Bydgoszczy\n' \
                '- usługa świadczona przez PUK CORIMP Sp. z o.o. \nw Bydgoszczy (wersja beta)'
            self.developers = ['Krzysztof Odziomek']
            self.designers = ['Krzysztof Odziomek']
            self.website = 'https://odziom.ovh/'
            self.github = 'https://github.com/odziom91/ProWywoz/issues'

            # preload providers list
            self.list_providers = [
                (1, 'MKUO ProNatura Sp. z o.o.'),
                (2, 'PUK CORIMP Sp. z o.o. (wersja beta)')
            ]
            # preload ProNatura API
            self.pronatura = ProNatura_api()

            # preload Corimp API
            self.corimp = Corimp_api()

            # init application
            super().__init__(application_id='app.ProWywoz.odziom')
            self.connect('activate', self.on_activate)
        except Exception as e:
            logging.critical('Error with initialization!')
            raise Exception('!!! Critical error !!! This app will be closed!')

    def on_activate(self, app):
        try:
            # load ui file
            builder = Gtk.Builder()
            builder.add_from_file('./ui/pronatura.ui')

            # get ui window
            self.window = builder.get_object('ProNatura')
            if not self.window:
                print("BŁĄD: Nie znaleziono obiektu 'main_window' w pliku UI!")
                sys.exit(1)
        except Exception as e:
            logging.critical('Error with init UI!')
            raise Exception('!!! Critical error !!! This app will be closed!')

        try:
            # set app to window
            self.window.set_application(self)
            self.window.set_title(f'{self.app_name} {self.app_version}')

            # get widgets and set parameters
            self.img_logo = builder.get_object('img_logo')
            self.img_logo.set_filename('./gfx/prowywoz.png')
            
            self.btn_create_ics = builder.get_object('btn_create_ics')
            self.btn_download_pdf = builder.get_object('btn_download_pdf')
            self.btn_about = builder.get_object('btn_about')
            self.dd_providers = builder.get_object('dd_providers')
            self.dd_streets = builder.get_object('dd_streets')
            self.dd_buildings = builder.get_object('dd_buildings')

            # load providers
            self.load_providers()

            # connect signals
            self.btn_download_pdf.connect('clicked', self.download_pdf_file)
            self.btn_about.connect('clicked', self.about_app)
            self.dd_providers.connect('notify::selected', self.load_streets)
            self.dd_streets.connect('notify::selected', self.load_buildings)

            self.dd_streets.set_selected(1)
            self.dd_streets.set_sensitive(True)

            # add search possibility for streets
            expression = Gtk.PropertyExpression.new(Gtk.StringObject, None, "string")
            self.dd_streets.set_expression(expression)
        except Exception as e:
            self.error_dialog('Error', str(e))
            logging.error(f'Error: {str(e)}')

        # show window
        self.window.present()
    
    def about_app(self, button):
        # about dialog
        ab = Adw.AboutDialog(
            title=f'{self.app_name} {self.app_version}',
            application_name=self.app_name,
            version=self.app_version,
            comments=self.app_comments,
            developers=self.developers,
            license_type=Gtk.License.GPL_3_0,
            website=self.website,
            application_icon='app.ProWywoz.odziom',
            designers=self.designers,
            issue_url=self.github
            )
        ab.present()

    def load_providers(self):
        # load providers to the drop down menu
        self.providers_gtk_list = Gtk.StringList()
        self.providers_gtk_list.append('Nie wybrano z listy')

        for provider in self.list_providers:
            _, provider_name = provider
            self.providers_gtk_list.append(provider_name)

        self.dd_providers.set_model(self.providers_gtk_list)
        self.dd_providers.set_selected(0)
        self.dd_providers.set_sensitive(True)

    def load_streets(self, dropdown, *args):
        # load streets to the drop down menu
        try:
            selected_pos = dropdown.get_selected()
            model = self.dd_providers.get_model()
            selected_provider = model[selected_pos].get_string()
            for provider in self.list_providers:
                provider_id, provider_name = provider
                if provider_name == selected_provider:
                    self.provider = provider_id
            match self.provider:
                case 1:
                    # download streets
                    self.streets = self.pronatura.dl_streets()
                    # update dropdown box with entries
                    self.streets_gtk_list = Gtk.StringList()
                    for street in self.streets:
                        self.streets_gtk_list.append(street['street'])
                    self.dd_streets.set_model(self.streets_gtk_list)
                case 2:
                    # download streets
                    self.streets = self.corimp.dl_streets()
                    # update dropdown box with entries
                    self.streets_gtk_list = Gtk.StringList()
                    for street in self.streets:
                        self.streets_gtk_list.append(street['value'])
                    self.dd_streets.set_model(self.streets_gtk_list)
        except requests.exceptions.ConnectionError as e:
            self.error_dialog('Błąd', f'{str(e)}')
        except requests.exceptions.HTTPError as e:
            self.error_dialog('Błąd', f'{str(e)}')
        except TypeError as e:
            if str(e) == "'NoneType' object is not subscriptable":
                self.error_dialog('Błąd', 'Nie wybrano wszystkich wymaganych pól.')
                logging.error(f'Error: Nie wybrano wszystkich wymaganych pól. {str(e)}')
        except Exception as e:
            self.error_dialog('Error', str(e))
            logging.error(f'Error: {str(e)}')

    def load_buildings(self, dropdown, *args):
        # load buildings to the drop down menu
        try:
            match self.provider:
                case 1:
                    selected_pos = dropdown.get_selected()
                    model = self.dd_streets.get_model()
                    selected_street = model[selected_pos].get_string()
                    for street in self.streets:
                        if selected_street == street['street']:
                            street_id = street['id']

                    self.buildings = self.pronatura.dl_buildings(street_id)
                    self.buildings_gtk_list = Gtk.StringList()
                    self.buildings_gtk_list.append('Nie wybrano z listy')
                    for building in self.buildings:
                        self.buildings_gtk_list.append(building['buildingNumber'])

                    self.dd_buildings.set_model(self.buildings_gtk_list)
                    self.dd_buildings.set_selected(0)
                    self.dd_buildings.set_sensitive(True)
                case 2:
                    selected_pos = dropdown.get_selected()
                    model = self.dd_streets.get_model()
                    selected_street = model[selected_pos].get_string()
                    for street in self.streets:
                        if selected_street == street['value']:
                            street_id = street['id']
                    
                    self.buildings = self.corimp.dl_buildings(street_id)
                    self.buildings_gtk_list = Gtk.StringList()
                    self.buildings_gtk_list.append('Nie wybrano z listy')

                    for building in self.buildings:
                        self.buildings_gtk_list.append(building['value'])
                    
                    self.dd_buildings.set_model(self.buildings_gtk_list)
                    self.dd_buildings.set_selected(0)
                    self.dd_buildings.set_sensitive(True)
        except requests.exceptions.ConnectionError as e:
            self.error_dialog('Błąd', f'{str(e)}')
        except requests.exceptions.HTTPError as e:
            self.error_dialog('Błąd', f'{str(e)}')
        except TypeError as e:
            if str(e) == "'NoneType' object is not subscriptable":
                self.error_dialog('Błąd', 'Nie wybrano wszystkich wymaganych pól.')
                logging.error(f'Error: Nie wybrano wszystkich wymaganych pól. {str(e)}')
        except Exception as e:
            self.error_dialog('Error', str(e))
            logging.error(f'Error: {str(e)}')

    def download_pdf_file(self, button):
        # download pdf file
        try:
            match self.provider:
                case 1:
                    selected_pos = self.dd_buildings.get_selected()
                    model = self.dd_buildings.get_model()
                    selected_building = model[selected_pos].get_string()
                    for building in self.buildings:
                        if selected_building == building['buildingNumber']:
                            self.building_id = building['id']
                    
                    # set filter for files
                    file_filter = Gtk.FileFilter()
                    file_filter.set_name("Pliki PDF")
                    file_filter.add_pattern("*.pdf")
                    filters = Gio.ListStore.new(Gtk.FileFilter)
                    filters.append(file_filter)

                    # set up save dialog window
                    save_dialog = Gtk.FileDialog()
                    save_dialog.set_title('Zapisz harmonogram do pliku PDF jako...')
                    save_dialog.set_initial_name('harmonogram.pdf')
                    save_dialog.set_filters(filters)
                    save_dialog.set_default_filter(file_filter)

                    save_dialog.save(self.window, None, self.pronatura.save_pdf, self.building_id)

                case 2:
                    selected_pos = self.dd_buildings.get_selected()
                    model = self.dd_buildings.get_model()
                    selected_building = model[selected_pos].get_string()
                    for building in self.buildings:
                        if selected_building == building['value']:
                            self.building_id = building['id']
                    
                    # set filter for files
                    file_filter = Gtk.FileFilter()
                    file_filter.set_name("Pliki PDF")
                    file_filter.add_pattern("*.pdf")
                    filters = Gio.ListStore.new(Gtk.FileFilter)
                    filters.append(file_filter)

                    # set up save dialog window
                    save_dialog = Gtk.FileDialog()
                    save_dialog.set_title('Zapisz harmonogram do pliku PDF jako...')
                    save_dialog.set_initial_name('harmonogram.pdf')
                    save_dialog.set_filters(filters)
                    save_dialog.set_default_filter(file_filter)

                    save_dialog.save(self.window, None, self.corimp.save_pdf, self.building_id)
        except requests.exceptions.ConnectionError as e:
            self.error_dialog('Błąd', f'{str(e)}')
        except requests.exceptions.HTTPError as e:
            self.error_dialog('Błąd', f'{str(e)}')
        except TypeError as e:
            if str(e) == "'NoneType' object is not subscriptable":
                self.error_dialog('Błąd', 'Nie wybrano wszystkich wymaganych pól.')
                logging.error(f'Error: Nie wybrano wszystkich wymaganych pól. {str(e)}')
        except AttributeError as e:
            if 'building_id' in str(e):
                self.error_dialog('Błąd', 'Nie wybrano numeru budynku.')
                logging.error(f'Error: Nie wybrano numeru budynku. {str(e)}')
        except Exception as e:
            self.error_dialog('Error', str(e))
            logging.error(f'Error: {str(e)}')
        
    def error_dialog(self, t, b):
        # error dialog
        err = Gtk.AlertDialog(
            buttons=['OK']
            )
        err.set_message(t)
        err.set_detail(b)
        err.show()

    def info_dialog(self, t, b):
        # info dialog
        ifo = Gtk.AlertDialog(
            buttons=['OK']
        )
        ifo.set_message(t)
        ifo.set_detail(b)
        ifo.show()
        
if __name__ == '__main__':
    try:
        # logs
        logging.basicConfig(
            filename='./log/ProWywoz.log',
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            encoding='utf-8'
        )

        logging.info('Starting application...')
        app = ProWywoz()
        app.run(sys.argv)
    except Exception as e:
        logging.critical(f'{str(e)}')