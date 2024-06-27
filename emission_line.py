


class EmissionLines(object):
    def __init__(self, spectrum):
        self.spectrum = spectrum
        self.grouped_lines = self.grouping_emission_lines()

        # Initialize emission list list
        self.line_list = []

    def grouping_emission_lines(self):
        """
            Groups blended emission lines together based off of ion, and a pre-determined tolerance
            (Note: this function assumes the DEM data is strictly increasing)
            Parameters: 
                        rest_lam_data: dataframe of emission lines
            Returns:
                        ion_groups: dictionary with ion name as the key, and  blended groups for that as the value
        """
        # Initialize variables
        tolerance = 10. 
        ion_groups = {}
        close_group_found = False

        # Loop through emission lines
        for _, row in self.spectrum.rest_lam_data.iterrows():
            ion = row["Ion"]
            wavelength = float(row["Wavelength"])

            # Check if wavelength is within wavelength bounds
            if wavelength < self.spectrum.min_wavelength: 
                continue

            # Check if ion does not exist in the dictionary
            if ion not in ion_groups:
                ion_groups[ion] = [[wavelength]]
                
            # Ion is already in the dictionary
            else:
                close_group_found = False
                # Iterate through each group for that ion
                for group in ion_groups[ion]:
                    # If the largest value in the group - wavelength is less than the tolerance, add to that group
                    if abs(max(group) - wavelength) <= tolerance:
                        group.append(wavelength)
                        close_group_found = True
                        break
                
                # If no close group was found, add to that ion as a seperate group
                if not close_group_found:
                    ion_groups[ion].append([wavelength])

        return ion_groups


    class Emission_Line: # MIGHT NOT NEED ME WE'LL SEE ????? IF I HAVE THE OBJECT
        def __init__(self, ion, group_lam, obs_lam, noise_bool, blended_bool, doppler_candidate, model_params, continuum, flux_error):
            self.ion = ion
            self.group_lam = group_lam
            self.obs_lam = obs_lam
            self.noise_bool = noise_bool
            self.blended_bool = blended_bool
            self.doppler_candidate = doppler_candidate
            self.model_params = model_params
            self.continuum = continuum
            self.flux_error = flux_error 

        def update_doppler_candidate(self, is_doppler_candidate):
            self.doppler_candidate = is_doppler_candidate
        
        def update_flux_error(self, new_flux, new_error):
            self.flux_error = [new_flux, new_error]

        def emission_line_to_dict(self):
            return {
                "wavelength_group": self.wavelength_group,
                "ion": self.ion,
                "obs_lam": float(self.obs_lam),
                "noise_bool": self.noise_bool,
                "blended_bool": self.blended_bool,
                "doppler_candidate": None,
                "fitted_model": None,
                "continuum": float(self.continuum),
                "flux_error": self.flux_error
            }