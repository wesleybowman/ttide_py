# Autogenerated with SMOP version 0.23
# main.py ../t_tide1.3/t_demo.m -o ../t_tide_py/t_demo.py
from __future__ import division
import numpy as np
from scipy.io import loadmat,savemat
import os

# T_DEMO - demonstration of capabilities.
# Short example of capabilities of tidal analysis toolbox.
#
# In this example, we 
#         a) do nodal corrections for satellites, 
#         b) use inference for P1 and K2, and
#         c) force a fit to a shallow-water constituent.
# Version 1.0
echo('on')
echo('on')
# Load the example.
load('t_example')
# Define inference parameters.
infername = np.array(['P1', 'K2']).reshape(1, -1)
inferfrom = np.array(['K1', 'S2']).reshape(1, -1)
infamp = np.array([0.33093, 0.27215]).reshape(1, -1)
infphase = np.array([- 7.07, - 22.4]).reshape(1, -1)
# The call (see t_demo code for details).
tidestruc, pout = t_tide(tuk_elev, 'interval', 1, 'start', tuk_time(1), 'latitude', 69 + 27 / 60, 'inference', infername, inferfrom, infamp, infphase, 'shallow', 'M10', 'error', 'linear', 'synthesis', 1) # nargout=2
# Use SNR=1 for synthesis. 
echo('off')
#    pout=t_predic(tuk_time,tidestruc,,...
#                  'latitude',69+27/60,...
#                  'synthesis',1);
clf
orient('tall')
subplot(411)
plot(tuk_time - datenum(1975, 1, 0), np.array([tuk_elev, pout]).reshape(1, -1))
line(tuk_time - datenum(1975, 1, 0), tuk_elev - pout, 'linewi', 2, 'color', 'r')
xlabel('Days in 1975')
ylabel('Elevation (m)')
text(190, 5.5, 'Original Time series', 'color', 'b')
text(190, 4.75, 'Tidal prediction from Analysis', 'color', np.array([0, 0.5, 0]).reshape(1, -1))
text(190, 4.0, 'Original time series minus Prediction', 'color', 'r')
title('Demonstration of t\\_tide toolbox')
subplot(412)
fsig = tidestruc.tidecon(:, 1) > tidestruc.tidecon(:, 2)
# Significant peaks
semilogy(np.array([tidestruc.freq(not  fsig), tidestruc.freq(not  fsig)]).reshape(1, -1).T, np.array([np.dot(0.0005, ones(sum_(not  fsig), 1)), tidestruc.tidecon(not  fsig, 1)]).reshape(1, -1).T, '.-r')
line(np.array([tidestruc.freq(fsig), tidestruc.freq(fsig)]).reshape(1, -1).T, np.array([np.dot(0.0005, ones(sum_(fsig), 1)), tidestruc.tidecon(fsig, 1)]).reshape(1, -1).T, 'marker', '.', 'color', 'b')
line(tidestruc.freq, tidestruc.tidecon(:, 2), 'linestyle', ':', 'color', np.array([0, 0.5, 0]).reshape(1, -1))
set_(gca, 'ylim', np.array([0.0005, 1]).reshape(1, -1), 'xlim', np.array([0, 0.5]).reshape(1, -1))
xlabel('frequency (cph)')
text(tidestruc.freq, tidestruc.tidecon(:, 1), tidestruc.name, 'rotation', 45, 'vertical', 'base')
ylabel('Amplitude (m)')
text(0.27, 0.4, 'Analyzed lines with 95\n % significance level')
text(0.35, 0.2, 'Significant Constituents', 'color', 'b')
text(0.35, 0.1, 'Insignificant Constituents', 'color', 'r')
text(0.35, 0.05, '95\n % Significance Level', 'color', np.array([0, 0.5, 0]).reshape(1, -1))
subplot(413)
errorbar(tidestruc.freq(not  fsig), tidestruc.tidecon(not  fsig, 3), tidestruc.tidecon(not  fsig, 4), '.r')
hold('on')
errorbar(tidestruc.freq(fsig), tidestruc.tidecon(fsig, 3), tidestruc.tidecon(fsig, 4), 'o')
hold('off')
set_(gca, 'ylim', np.array([- 45, 360 + 45]).reshape(1, -1), 'xlim', np.array([0, 0.5]).reshape(1, -1), 'ytick', np.array([0:360]).reshape(1, -1))
xlabel('frequency (cph)')
ylabel('Greenwich Phase (deg)')
text(0.27, 330, 'Analyzed Phase angles with 95\n % CI')
text(0.35, 290, 'Significant Constituents', 'color', 'b')
text(0.35, 250, 'Insignificant Constituents', 'color', 'r')
subplot(414)
ysig = tuk_elev
yerr = tuk_elev - pout
nfft = 389
bd = isnan(ysig)
gd = find(not  bd)
bd(np.array([1:(min_(gd)-1), (max_(gd)+1):end]).reshape(1, -1)) = 0
ysig(bd) = interp1(gd, ysig(gd), find(bd))
#[Pxs,F]=psd(ysig(isfinite(ysig)),nfft,1,[],ceil(nfft/2));
Pxs, F = pwelch(ysig(isfinite(ysig)), hanning(nfft), ceil(nfft / 2), nfft, 1) # nargout=2
Pxs = Pxs / 2
#[Pxso,Fo]=psd(ysig(isfinite(ysig)),nfft,1,[],ceil(nfft/2));
#[Pxs,F]=pmtm(ysig(isfinite(ysig)),4,4096,1);
yerr(bd) = interp1(gd, yerr(gd), find(bd))
#[Pxe,F]=psd(yerr(isfinite(ysig)),nfft,1,[],ceil(nfft/2));
Pxe, F = pwelch(yerr(isfinite(ysig)), hanning(nfft), ceil(nfft / 2), nfft, 1) # nargout=2
Pxe = Pxe / 2
#[Pxe,F]=pmtm(yerr(isfinite(ysig)),4,4096,1);
semilogy(F, Pxs)
line(F, Pxe, 'color', 'r')
xlabel('frequency (cph)')
ylabel('m^2/cph')
text(0.17, 10000.0, 'Spectral Estimates before and after removal of tidal energy')
text(0.35, 1000.0, 'Original (interpolated) series', 'color', 'b')
text(0.35, 100.0, 'Analyzed Non-tidal Energy', 'color', 'r')
