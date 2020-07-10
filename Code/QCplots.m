%% load data

addpath(genpath('/Users/Michael/Documents/Work/UNSW/Work/'))
addpath(genpath('/Volumes/Hemming_backup/UNSW_work/'))

filename = (['/Users/Michael/Documents/Work/UNSW/Work/QC_reports/',...
    'IMOS_ANMN-NSW_TZ_20091029_PH100_FV01_TEMP-aggregated-timeseries_END-20190612_C-20190819.nc']);
data = get_mooring(filename,1);

load('CTD_TEMP_PortHacking.mat');



%% Mooring vs CTD data plot

T_CTD = CTD_TEMP.TEMP(CTD_TEMP.STATION == 1808);
D_CTD = CTD_TEMP.DEPTH(CTD_TEMP.STATION == 1808);
t_CTD = CTD_TEMP.TIME(CTD_TEMP.STATION == 1808);
ID_CTD = CTD_TEMP.SITE_index(CTD_TEMP.STATION == 1808);

check_mooring = data.TIME >= nanmean(t_CTD)-0.0417 & data.TIME <= nanmean(t_CTD)+0.0417;

% bin mooring profile
[data] = get_NDmat(data);
[binned_profile] = bin_mooring_profile(data.TEMP(check_mooring),data.DEPTH(check_mooring),data.NOMINAL_DEPTH_mat(check_mooring));

% create figure
figure('units','normalized','position',[.1 .3 .4 1]);

m = scatter(data.TEMP(check_mooring),data.DEPTH(check_mooring),'filled','MarkerFaceColor',[.8 .8 .8],'MarkerEdgeColor',[.8 .8 .8])
hold on
check_CTD = ID_CTD == 1;
C = plot(T_CTD(check_CTD),D_CTD(check_CTD),'LineWidth',2,'Color',[1 .4 .2]);
check_CTD = ID_CTD == 4;
plot(T_CTD(check_CTD),D_CTD(check_CTD),'LineWidth',2,'Color',[1 .4 .2]);
Mi = plot(binned_profile.VAR_int,binned_profile.DEPTH_int,'LineWidth',2,'Color',[.2 .6 .6]);
scatter(binned_profile.VAR,binned_profile.DEPTH,75,'MarkerFaceColor','k','MarkerEdgeColor','k');
scatter(binned_profile.VAR,binned_profile.DEPTH,50,'MarkerFaceColor',[.2 .6 .6],'MarkerEdgeColor',[.2 .6 .6]);

set(gca,'YDir','Reverse','Box','On','LineWidth',2,'FontSize',20);   
leg = legend([m Mi C],'Mooring','Mooring (binned)','CTD (NRSPHB & PH100)');
set(leg,'Location','SouthEast','Box','Off');
ylim([0 112]);
xlabel('Temperature [^\circC]');
ylabel('Depth [m]');

print(gcf,'-dpng','-r400',['/Users/Michael/Documents/Work/UNSW/Work/QC_reports/plots/','MvsCTDprof.png']);

%% climatology plot

[~,mns,dys,~,~,~] = datevec(data.TIME);
YD = datenum(0,mns,dys);
% 16m nominal depth
check_16 = data.NOMINAL_DEPTH_mat == 16;
% produce simple climatology
for day = 1:366
    day
    if day == 1
        check = YD == 1 | YD == 2 | YD == 3 | YD == 366 | YD == 365;
    end
    if day == 2
        check = YD == 1 | YD == 2 | YD == 3 | YD == 4 | YD == 366;
    end
    if day == 365
        check = YD == 363 | YD == 364 | YD == 365 | YD == 366 | YD == 1;
    end
    if day == 366
        check = YD == 364 | YD == 365 | YD == 366 | YD == 1 | YD == 2;
    end    
    if day > 2 & day < 365    
         check = YD >= day-2 & YD <= day+2;
    end
    clim.T(day) = nanmean(data.TEMP(check & check_16));
    clim.P90(day) = prctile(data.TEMP(check & check_16),90);
    clim.P10(day) = prctile(data.TEMP(check & check_16),10);
end
clim.t = 1:366;

% create figure
figure('units','normalized','position',[.1 .3 1 .7]);
% climatology plot
subplot(10,10,[1:6,11:16,21:26,31:36,41:46,51:56,61:66,71:76,81:86,91:96])
s1 = scatter(YD(check_16),data.TEMP(check_16),10,'filled','MarkerFaceColor',[.8 .8 .8],'MarkerEdgeColor',[.8 .8 .8])
hold on
check_deployment = data.TIME > datenum(2019,03,01) & data.TIME < datenum(2019,06,01);
s2 = scatter(YD(check_deployment & check_16),data.TEMP(check_deployment & check_16),10,'filled','MarkerFaceColor',[.4 .8 0],'MarkerEdgeColor',[.4 .8 0])
c = plot(clim.T,'LineWidth',3,'Color','k','LineStyle',':')
c90 = plot(clim.P90,'LineWidth',3,'Color','r','LineStyle',':')
c10 = plot(clim.P10,'LineWidth',3,'Color','b','LineStyle',':')

leg = legend([s1 s2 c c10 c90],'Mooring 16 m 03/03/2011 - 12/06/2019','Mooring 16 m 1903',...
    'Mean 16 m 2011-2019','10th percentile 16 m 2011-2019','90th percentile 16 m 2011-2019');
set(leg,'Box','Off','FontSize',20)
set(gca,'FontSize',22,'Box','On'); xlim([-2 369])
datetick('x','KeepLimits'); ylabel('Temperature [^\circC]');
title('PH100 16 m');

% depth distribution plot
subplot(10,10,[8:10,18:20,28:30,38:40,48:50,58:60,68:70,78:80,88:90,98:100])
hold on;
% mooring data all
[n,edges] = histcounts(data.DEPTH(check_16),50)
max_all = nanmax(n);
n_perc = n./sum(n)*100;
n_norm = (1/max_all)*n;
edges = interp1(1:51,edges,1.5:1:50.5,'Linear');
% patch(n_perc,edges,[.8 .8 .8]);
% scatter(n_perc(n_perc > 0.5),edges(n_perc > 0.5),'k','filled');
b1 = barh(edges,n_norm)

% mooring data deployment
[n,edges] = histcounts(data.DEPTH(check_deployment & check_16),20)
n_norm = (1/max(n))*n;
n_perc = n./sum(n)*100;
edges = interp1(1:21,edges,1.5:1:20.5,'Linear');
b2 = barh(edges,n_norm)

% set properties
set(b1,'FaceColor',[.8 .8 .8]);
set(b2,'FaceColor',[.4 .8 0]);
set(gca,'YLim',[8 30],'XLim',[0 1.1],'FontSize',22,'Box','On','YDir','Reverse');
add_l(16,1);
xlabel('Number of points (normalised)');
ylabel('Depth [m]');
leg = legend([b1 b2],'Mooring 16 m 03/03/2011 - 12/06/2019','Mooring 16 m 1903');
set(leg,'Location','SouthEast','Box','Off','FontSize',14);

print(gcf,'-dpng','-r400',['/Users/Michael/Documents/Work/UNSW/Work/QC_reports/plots/','climatology_example.png']);

%% example of instrument selection

figure('units','normalized','position',[.1 .3 .8 .7]);

s0 = scatter(data.TIME(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3), ...
    data.DEPTH(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3),10,'k','filled');
hold on;
check_instrument = data.SERIAL_NUMBER == 23500;
s1 = scatter(data.TIME(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3 & check_instrument), ...
    data.DEPTH(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3 & check_instrument),10,'r','filled');
check_instrument = data.SERIAL_NUMBER == 23664;
s2 = scatter(data.TIME(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3 & check_instrument), ...
    data.DEPTH(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3 & check_instrument),10,'g','filled');
check_instrument = data.SERIAL_NUMBER == 23501;
s3 = scatter(data.TIME(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3 & check_instrument), ...
    data.DEPTH(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3 & check_instrument),10,'b','filled');
check_instrument = data.SERIAL_NUMBER == 231288;
s4 = scatter(data.TIME(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3 & check_instrument), ...
    data.DEPTH(data.TEMP_quality_control < 3 & data.DEPTH_quality_control < 3 & check_instrument),10,'y','filled');

leg = legend([s0 s1 s2 s3 s4],'All data','023-500 520PT','023-664 520T','023-501 520PT','023-1288 520T');

set(leg,'Box','Off','FontSize',20,'Orientation','Horizontal','Location','SouthWest');
set(gca,'YDir','Reverse','FontSize',20,'LineWidth',2,'Box','On'); ylim([5 125]);
datetick('x','KeepLimits');
title('PH100');

print(gcf,'-dpng','-r400',['/Users/Michael/Documents/Work/UNSW/Work/QC_reports/plots/','instrument_lookup_example.png']);

%% velocity time-depth plot

filename = (['/Users/Michael/Documents/Work/UNSW/Work/QC_reports/',...
    'IMOS_ANMN-NSW_VZ_20080625_SYD100_FV01_velocity-aggregated-timeseries_END-20200114_C-20200312.nc']);
data_vel = get_mooring(filename,1);

check = data_vel.TIME > datenum(2019,03,01) & data_vel.TIME < datenum(2019,06,01);

figure('units','normalized','position',[.1 .3 .8 .7]);

subplot(2,1,1)
scatter(data_vel.TIME(check),data_vel.DEPTH(check), ...
    30,data_vel.VCUR(check),'filled','Sq')
caxis([-0.5 0.5]); cmocean('balance');
ylim([-5 100])
set(gca,'YDir','Reverse','LineWidth',2,'Box','On','FontSize',16);
datetick('x','KeepLimits'); ylabel('Depth [m]');
cb = colorbar;
ylabel(cb,'VCUR [m s^{-1}]');
title('VCUR without QC');

subplot(2,1,2)
scatter(data_vel.TIME(check & data_vel.VCUR_quality_control <3),data_vel.DEPTH(check & data_vel.VCUR_quality_control <3), ...
    30,data_vel.VCUR(check & data_vel.VCUR_quality_control <3),'filled','Sq')
caxis([-0.5 0.5]); cmocean('balance');
ylim([-5 100])
set(gca,'YDir','Reverse','LineWidth',2,'Box','On','FontSize',16);
datetick('x','KeepLimits'); ylabel('Depth [m]');
cb = colorbar;
ylabel(cb,'VCUR [m s^{-1}]');
title('VCUR with QC');

print(gcf,'-dpng','-r400',['/Users/Michael/Documents/Work/UNSW/Work/QC_reports/plots/','VCUR_QC_example.png']);

