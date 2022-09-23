/*
 *	PDCFUNC.h
 *	Photron Device Control SDK
 *	Function Definition
 *
 *	Copyright (C) 2006-2012 PHOTRON LIMITED
 */

#ifndef	_PDC_FUNC_H_
#define	_PDC_FUNC_H_

#ifdef	__cplusplus
extern "C" {
#endif	/*	__cplusplus	*/

/*
 *	Initialize etc...
 */
unsigned long WINAPI
PDC_Init(
		unsigned long 			*pErrorCode
		);

unsigned long WINAPI
PDC_DetectDevice(
		unsigned long			nInterfaceCode,
		unsigned long			*pDetectNo,
		unsigned long			nDetectNum,
		unsigned long			nDetectParam,
		PPDC_DETECT_NUM_INFO	pDetectNumInfo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_DetectDeviceLV(
		unsigned long			nInterfaceCode,
		unsigned long			*pDetectNo,
		unsigned long			nDetectNum,
		unsigned long			nDetectParam,
		unsigned long			*pDeviceNum,
		unsigned long			*pDeviceCode,
		unsigned long			*pTmpDeviceNo,
		unsigned long			*pInterfaceCode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_OpenDevice(
		PPDC_DETECT_INFO		pDetectInfo,
		unsigned long			*pDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_OpenDevice2(
		PPDC_DETECT_INFO		pDetectInfo,
		long					nMaxRetryCount,
		long					nConnectMode,
		unsigned long			*pDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_OpenDeviceLV(
		unsigned long			nDeviceCode,
		unsigned long			nTmpDeviceNo,
		unsigned long			nInterfaceCode,
		unsigned long			*pDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_OpenDevice2LV(
		unsigned long			nDeviceCode,
		unsigned long			nTmpDeviceNo,
		unsigned long			nInterfaceCode,
		long					nMaxRetryCount,
		long					nConnectMode,
		unsigned long			*pDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_CloseDevice(
		unsigned long			nDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDeviceNameA(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					*pStrName,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_GetDeviceNameW(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		wchar_t					*pStrName,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_GetDeviceName  PDC_GetDeviceNameW
#else
#define PDC_GetDeviceName  PDC_GetDeviceNameA
#endif // !UNICODE

unsigned long WINAPI
PDC_GetSubInterface(
		unsigned long			nDeviceNo,
		unsigned long			*pIPAddress,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_OpenSubInterface(
		unsigned long			nDeviceNo,
		unsigned long			*pIPAddress,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_OpenSubInterface2(
		unsigned long			nDeviceNo,
		long					nMaxRetryCount,
		long					nConnectMode,
		unsigned long			*pIPAddress,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_CloseSubInterface(
		unsigned long			nDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetNumberOfDevice(
		unsigned long			*pNum,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_IsFunction(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nFunction,
		char					*pFlag,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetInterfaceInfo(
		unsigned long			nInterfaceCode,
		unsigned long			nParam1,
		unsigned long			nParam2,
		unsigned long			nParam3,
		unsigned long			nParam4,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetInterfaceInfo(
		unsigned long			nInterfaceCode,
		unsigned long			*pParam1,
		unsigned long			*pParam2,
		unsigned long			*pParam3,
		unsigned long			*pParam4,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_DeviceStatusUpdate(
		unsigned long			nDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_PingDevice(
		unsigned long			nDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetConnectStatus(
		unsigned long			nDeviceNo,
		unsigned long			*pStatus,
		unsigned long			*pErrorCode
);

/*
 *	Get List
 */
unsigned long WINAPI
PDC_GetRecordRateList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetResolutionList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShutterSpeedFpsList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShutterSpeedUsecList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShutterSpeedNsecList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetTriggerModeList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSensorGainModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSensorGammaModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetColorTempModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLUTModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableRecordRateList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDSShutterModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVideoOutModeList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShadingModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetAEShutterFpsList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetAEShutterUsecList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetAEShutterNsecList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetEdgeEnhanceModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExternalIOTypeList(
	unsigned long			nDeviceNo,
	unsigned long		   nMode,
	unsigned long			*pSize,
	unsigned long			*pList,
	unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_GetExternalInModeList(
		unsigned long			nDeviceNo,
		unsigned long			nPortNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExternalOutModeList(
		unsigned long			nDeviceNo,
		unsigned long			nPortNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSyncPriorityList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExistChildDeviceList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetOpenedDeviceList(
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLUTValueList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nPlane,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLUTOrgValueList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nPlane,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetPartitionList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pCount,
		unsigned long			*pFrames,
		unsigned long			*pBlocks,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetProgSwitchModeList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetPixelGainModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSyncOutTimesList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExposeOutTimesList(
		unsigned long			nDeviceNo,
		unsigned long			nSignal,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetColorEnhanceModeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetHeadExchangeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_GetLiveResolutionList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetCameraCommandBaudRateList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDownloadModeList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVideoOutSignalList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVideoOutHDSDIList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetHighSpeedModeList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetBlackClipLevelList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetRecordingTypeList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetADCRangeList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetPartitionIncModeList(
		unsigned long			nDeviceNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);


/*
 *	Set List
 */
unsigned long WINAPI
PDC_SetLUTValueList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nPlane,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetPartitionList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nCount,
		unsigned long			*pBlocks,
		unsigned long			*pErrorCode
		);

/*
 *	Get Device status
 */
unsigned long WINAPI
PDC_GetDeviceCode(
		unsigned long			nDeviceNo,
		unsigned long			*pCode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDeviceID(
		unsigned long			nDeviceNo,
		unsigned long			*pID,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetProductID(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pID,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLotID(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pID,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetIndividualID(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pID,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVersion(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pVer,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetColorType(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetStatus(
		unsigned long			nDeviceNo,
		unsigned long			*pStatus,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShutterLockMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetResolutionLockMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetPartitionIncMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetKeyPadLock(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVideoOutMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetChildDeviceCount(
		unsigned long			nDeviceNo,
		unsigned long			*pCount,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMaxChildDeviceCount(
		unsigned long			nDeviceNo,
		unsigned long			*pCount,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExternalCount(
		unsigned long			nDeviceNo,
		unsigned long			*pIn,
		unsigned long			*pOut,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExternalInMode(
		unsigned long			nDeviceNo,
		unsigned long			nPort,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExternalOutMode(
		unsigned long			nDeviceNo,
		unsigned long			nPort,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetIRIG(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMCDL(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetADC(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetADCRange(
		unsigned long			nDeviceNo,
		unsigned long			nADCChannel,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetIRIGOffset(
		unsigned long			nDeviceNo,
		long					*pValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetIRIGSampleMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_GetRecordRate(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pRate,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetTriggerMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pAFrames,
		unsigned long			*pRFrames,
		unsigned long			*pRCount,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetResolution(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetResolutionROI(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShutterSpeedFps(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pFps,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShutterSpeedUsec(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pUsec,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShutterSpeedNsec(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pNsec,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMaxPartition(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pCount,
		unsigned long			*pBlock,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetCurrentPartition(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSensorGainMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSensorGammaMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetColorTempMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pR,
		unsigned long			*pG,
		unsigned long			*pB,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSoftColorTempMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pR,
		unsigned long			*pG,
		unsigned long			*pB,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetAutoExposure(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLUTMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDSShutterMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDSShutterValue(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetEdgeEnhanceMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShadingMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShadingTypeList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pSize,
		unsigned long			*pList,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetPixelGainMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMaxFrames(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pFrames,
		unsigned long			*pBlocks,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMaxResolution(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSegmentPosition(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pXPos,
		unsigned long			*pYPos,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableMaxResolution(
		unsigned long			nDeviceNo,
		unsigned long			nRate,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableMaxWidth(
		unsigned long			nDeviceNo,
		unsigned long			nRate,
		unsigned long			nHeight,
		unsigned long			*pWidth,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableMaxHeight(
		unsigned long			nDeviceNo,
		unsigned long			nRate,
		unsigned long			nWidth,
		unsigned long			*pHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableMaxRate(
		unsigned long			nDeviceNo,
		unsigned long			nWidth,
		unsigned long			nHeight,
		unsigned long			*pRate,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableChannel(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pChannel,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableChannelInfo(
		unsigned long			nDeviceNo,
		unsigned long			nChannel,
		unsigned long			*pRate,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pXPos,
		unsigned long			*pYPos,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableChannelInfo2(
		unsigned long			nDeviceNo,
		unsigned long			nChannel,
		unsigned long			*pRate,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pXPos,
		unsigned long			*pYPos,
		unsigned long			*pIRIG,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableChannelInfo3(
		unsigned long			nDeviceNo,
		unsigned long			nChannel,
		unsigned long			*pRate,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pXPos,
		unsigned long			*pYPos,
		unsigned long			*pIRIG,
		unsigned long			*pHSMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetEnableVariableChannelSetting(
		unsigned long			nDeviceNo,
		unsigned long			pRate,
		unsigned long			pWidth,
		unsigned long			pHeight,
		unsigned long			*pEnable,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetAutoExposureInfo(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pXPos,
		unsigned long			*pYPos,
		unsigned long			*pValue,
		unsigned long			*pRange,
		unsigned long			*pLimit,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMaxBitDepth(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					*pDepth,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLUTParams(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nLUTMode,
		PPDC_LUT_PARAMS			pParams,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDelay(
		unsigned long			nDeviceNo,
		unsigned long			nSignal,
		unsigned long			*pValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDelayLimit(
		unsigned long			nDeviceNo,
		unsigned long			nSignal,
		unsigned long			*pValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDelayLimitEx(
		unsigned long			nDeviceNo,
		unsigned long			nSignal,
		unsigned long			*pValue_max,
		unsigned long			*pValue_min,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVariableRestriction(
		unsigned long			nDeviceNo,
		unsigned long			*pWidthStep,
		unsigned long			*pHeightStep,
		unsigned long			*pXPosStep,
		unsigned long			*pYPosStep,
		unsigned long			*pWidthMin,
		unsigned long			*pHeightMin,
		unsigned long			*pFreePos,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetColorEnhanceValue(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nPlane,
		long					*pR,
		long					*pG,
		long					*pB,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetColorEnhanceMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetDownloadMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetCamMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMaxFullResoRate(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pRate,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLowLightMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetProgSwitchMode(
		unsigned long			nDeviceNo,
		unsigned long			nSwitchNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetColorTempBase(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pBase,
		unsigned long			*pMax,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetAutoExposureRestriction(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidthStep,
		unsigned long			*pHeightStep,
		unsigned long			*pXPosStep,
		unsigned long			*pYPosStep,
		unsigned long			*pWidthMin,
		unsigned long			*pHeightMin,
		unsigned long			*pMaxValue,
		unsigned long			*pMaxRange,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSyncOutTimes(
		unsigned long			nDeviceNo,
		unsigned long			*pRatio,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetStoreNum(
		unsigned long			nDeviceNo,
		unsigned long			*pNum,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetEthernetInfo(
		unsigned long			nDeviceNo,
		unsigned long			nTarget,
		unsigned long			*pValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetConnectedEthernetInfo(
		unsigned long			nDeviceNo,
		unsigned long			nTarget,
		unsigned long			*pValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetIRIGPhaseLock(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetIRIGPhaseLockStatus(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetHighSpeedMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetBurstTransfer(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetHeadExchange(
		unsigned long			nDeviceNo,
		unsigned long			*pNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetHeadTypeNameA(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nHeadNo,
		char					*pStrName,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_GetHeadTypeNameW(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nHeadNo,
		wchar_t					*pStrName,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_GetHeadTypeName  PDC_GetHeadTypeNameW
#else
#define PDC_GetHeadTypeName  PDC_GetHeadTypeNameA
#endif // !UNICODE

unsigned long WINAPI
PDC_GetStepShutter(
		unsigned long			nDeviceNo,
		unsigned long			*pStep,
		unsigned long			*pMin,
		unsigned long			*pMax,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_GetLiveResolutionMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetCameraCommandBaudRate(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pRate,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetBitDepth(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					*pDepth,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetBitDepth2(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					*pDepth,
		unsigned long			*pBitSel,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSyncPriority(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVideoOutSignal(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVideoOutSignalEnable(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetVideoOutHDSDI(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetRecordingType(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetPixelGainData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetAutoPlay(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetFactoryDefaults(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetStorePreset(
		unsigned long			nDeviceNo,
		unsigned long			*pNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetStorePresetReboot(
		unsigned long			nDeviceNo,
		unsigned long			*pReboot,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_GetInstructionSet(
		unsigned long			nDeviceNo,
		unsigned long			*pInstSetCode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLEDMode(
		unsigned long			nDeviceNo,
		unsigned long			*pLEDMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetBatteryPowerMode(
		unsigned long			nDeviceNo,
		unsigned long			*pBattery,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_GetSyncInSignalStatus(
		unsigned long			nDeviceNo,
		unsigned long			*pStatus,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLiveIRIGData(
		unsigned long			nDeviceNo,
		PPDC_IRIG_INFO			pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetPolarizerConfig(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetShadingType(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_GetShadingAvailable(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pAvailable,
		unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_GetBlackClipLevel(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSubInterfaceMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExposeExtension(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetImageTrigger(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetImageTriggerInfo(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pXPos,
		unsigned long			*pYPos,
		unsigned long			*pValue,
		unsigned long			*pRange,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetImageTriggerRestriction(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidthStep,
		unsigned long			*pHeightStep,
		unsigned long			*pXPosStep,
		unsigned long			*pYPosStep,
		unsigned long			*pWidthMin,
		unsigned long			*pHeightMin,
		unsigned long			*pMaxValue,
		unsigned long			*pMaxRange,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetImageTriggerConditions(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pConditions,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetRTC(
		unsigned long			nDeviceNo,
		unsigned long			*pYear,
		unsigned long			*pMonth,
		unsigned long			*pDay,
		unsigned long			*pHour,
		unsigned long			*pMinute,
		unsigned long			*pSecond,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemoryModePartition(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLensControl(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pType,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetGetherTransferMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMechaShutterMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

//Hieu ExposeTime
unsigned long WINAPI 
PDC_GetExposeTimeData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		UINT32					*pBuf,
		unsigned long			*pNum,
		unsigned long			*pErrorCode
		);

//hieu recon cmd 20131024
unsigned long WINAPI
PDC_GetCurrentFramesRecorded(
		unsigned long			nDevHandle,
		unsigned long			*pParam,
		unsigned long			*pErrorCode
		);

/*	FAN Control*/
unsigned long WINAPI
PDC_GetFanCtrl(
		unsigned long			nDeviceNo,
		unsigned long			*pCtrl,
		unsigned long			*pUsed,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetFanState(
		unsigned long			nDeviceNo,
		unsigned long			*pState,
		unsigned long			*pOnState,
		unsigned long			*pErrorCode
		);

/*	SD CARD Control*/
unsigned long WINAPI
PDC_GetSdCardCtrl(
		unsigned long 			nDeviceNo,
		unsigned long 			*pCtrl,
		unsigned long 			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSdCardState(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			*pInOut,
		unsigned long			*pProtect,
		unsigned long			*pFormat,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSdCardInfo(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			*pSpeedMode,
		unsigned long			*pSpeedClass,
		unsigned long			*pSize,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSdCardDataRecDate(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			nDataNo,
		unsigned long			*pDate,
		unsigned long			*pTime,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSdCardDataRecFrames(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			nDataNo,
		unsigned long			*pFrames,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSdCardMemoryMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetSdCardRunState(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			*pState,
		unsigned long			*pOption,
		unsigned long			*pErrorCode
		);

//
// SSD BOX
//
unsigned long WINAPI
PDC_GetSSDBoxInfo(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			*pTotal,
		unsigned long			*pAvailable,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_GetSSDBoxDataName(
		unsigned long nDeviceNo,
		unsigned long nSlotNo,
		unsigned long nDataNo,
		char *pName,
		unsigned long *pErrorCode
		);

unsigned long WINAPI 
PDC_SetSSDBoxDataName(
		unsigned long nDeviceNo,
		unsigned long nSlotNo,
		unsigned long nDataNo,
		char *pName,
		unsigned long *pErrorCode
		);

unsigned long WINAPI
PDC_GetSSDBoxCtrl(
		unsigned long 			nDeviceNo,
		unsigned long 			*pCtrl,
		unsigned long 			*pErrorCode
		);

//
// FAST Drive
//
unsigned long WINAPI
PDC_GetFASTDriveInfo(
	unsigned long			nDeviceNo,
	unsigned long			*pTotal,
	unsigned long			*pAvailable,
	unsigned long			*pErrorCode
	);

unsigned long WINAPI
PDC_GetFASTDriveInfo2(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			*pTotal,
	unsigned long			*pAvailable,
	unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_GetStorageMode(
	unsigned long			nDeviceNo,
	unsigned long			*pMode,
	unsigned long			*pErrorCode
	);

unsigned long WINAPI
PDC_GetFASTDriveState(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			*pInOut,
	unsigned long			*pFormat,
	unsigned long			*pErrorCode
	);

unsigned long WINAPI
PDC_GetFASTDriveDataName(
	unsigned long nDeviceNo,
	unsigned long nDataNo,
	char *pName,
	unsigned long *pErrorCode
	);

unsigned long WINAPI
PDC_GetFASTDriveDataName2(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	char *pName,
	unsigned long *pErrorCode
);

unsigned long WINAPI
PDC_SetFASTDriveDataName(
	unsigned long nDeviceNo,
	unsigned long nDataNo,
	char *pName,
	unsigned long *pErrorCode
	);

unsigned long WINAPI
PDC_SetFASTDriveDataName2(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	char *pName,
	unsigned long *pErrorCode
);

unsigned long WINAPI
PDC_GetFASTDriveCtrl(
	unsigned long 			nDeviceNo,
	unsigned long 			*pCtrl,
	unsigned long 			*pErrorCode
	);

unsigned long WINAPI
PDC_GetFASTDriveDataRecDate(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			nDataNo,
	unsigned long			*pDate,
	unsigned long			*pTime,
	unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_GetFASTDriveDataRecFrames(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			nDataNo,
	unsigned long			*pFrames,
	unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_SetFASTDriveFormatRequest(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_SetFASTDriveCancelRequest(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_SetFASTDriveResetRequest(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			*pErrorCode
);
unsigned long WINAPI
PDC_SetFASTDriveSaveRequest(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_GetFASTDriveRunState(
	unsigned long			nDeviceNo,
	unsigned long			nSlotNo,
	unsigned long			*pState,
	unsigned long			*pOption,
	unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_GetFASTDriveSaveSlotNo(
	unsigned long			nDeviceNo,
	unsigned long			nChildNo,
	unsigned long*			nSlotNo,
	unsigned long			*pErrorCode
);

//
// Media(CFast)
//
unsigned long WINAPI
PDC_SetMediaSaveRequest(
	unsigned long	nDeviceNo,
	unsigned long	nSlotNo,
	long			nStartFrame,
	long			nFrameCount,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_SetMediaCancelRequest(
	unsigned long	nDeviceNo,
	unsigned long	nSlotNo,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_GetMediaState(
	unsigned long	nDeviceNo,
	unsigned long	nSlotNo,
	unsigned long	*pInOut,
	unsigned long	*pProtect,
	unsigned long	*pFormat,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_GetMediaRunState(
	unsigned long	nDeviceNo,
	unsigned long	nSlotNo,
	unsigned long	*pState,
	unsigned long	*pOption,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_SetMediaFormatRequest(
	unsigned long	nDeviceNo,
	unsigned long	nSlotNo,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_GetMediaInfo(
	unsigned long	nDeviceNo,
	unsigned long	nSlotNo,
	PPDC_MEDIA_INFO	pInfo,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_GetMediaRecordInfo(
	unsigned long		nDeviceNo,
	unsigned long		nSlotNo,
	unsigned long		nDataNo,
	PPDC_RECORD_INFO	pRecInfo,
	unsigned long		*pErrorCode
);

unsigned long WINAPI PDC_OpenMedia(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long *pErrorCode
);

unsigned long WINAPI PDC_CloseMedia(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long *pErrorCode
);

unsigned long WINAPI PDC_GetMediaImage(
	unsigned long	nDeviceNo,
	unsigned long	nSlotNo,
	unsigned long	nDataNo,
	long			nFrameNo,
	unsigned long	nInterleave,
	void			*pData,
	unsigned long	*pErrorCode
);

/*
 *	Get Recorded status
 */
unsigned long WINAPI
PDC_GetMemIRIG(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemMCDL(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemADC(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemADCRange(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nADCChannel,
		unsigned long			*pMode,
		unsigned long			*pErrorCode);

unsigned long WINAPI
PDC_GetAdcInfo(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pNumberOfChannel,
		unsigned long			*pSamplePerFrame,
		unsigned long			*pErrorCode);

unsigned long WINAPI
PDC_GetMemRecordRate(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pRate,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemTriggerMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pAFrames,
		unsigned long			*pRFrames,
		unsigned long			*pRCount,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemResolution(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemResolutionROI(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pWidth,
		unsigned long			*pHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemShutterSpeedFps(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pFps,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemShutterSpeedUsec(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pUsec,
		unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_GetMemShutterSpeedNsec(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pNsec,
		unsigned long			*pErrorCode
);


unsigned long WINAPI
PDC_GetMemSensorGainMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemSensorGammaMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemColorTempMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pR,
		unsigned long			*pG,
		unsigned long			*pB,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemAutoExposure(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemLUTMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemDSShutterMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemDSShutterValue(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemEdgeEnhanceMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetTransferOption(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*p8BitSel,
		unsigned long			*pBayer,
		unsigned long			*pInterleave,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemFrameInfo(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		PPDC_FRAME_INFO			pFrame,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemColorEnhanceValue(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nPlane,
		long					*pR,
		long					*pG,
		long					*pB,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemColorEnhanceMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemIRIGPhaseLockStatus(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_GetMemLiveResolutionMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemBitDepth(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					*pDepth,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemBitDepth2(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					*pDepth,
		unsigned long			*pBitSel,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemSegmentPosition(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pXpos,
		unsigned long			*pYpos,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetInitialError(
		unsigned long			nDeviceNo,
		unsigned long			nHeadCount,
		unsigned long			*pErrorNumber,
		unsigned long			*pErrorOption,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_GetLastError(
		unsigned long			nDeviceNo,
		unsigned long			*pType,
		unsigned long			*pErrorNumber,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_GetIgnoreTriggerNumber(
		unsigned long			nDeviceNo,
		unsigned long			*pNumber,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetExtSyncOverSync(
		unsigned long			nDeviceNo,
		unsigned long			*pStatus,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetHeadLedLaser(
		unsigned long 			nDeviceNo,
		unsigned long 			nChildNo,
		unsigned long 			*pLedStatus,
		unsigned long 			*pLaserStatus,
		unsigned long 			*pErrorCode
		);
unsigned long WINAPI
PDC_GetLensInfo(
		unsigned long 			nDeviceNo,
		unsigned long 			nChildNo,
		unsigned long 			*pLensType,
		unsigned long 			*pErrorCode
		);
unsigned long WINAPI
PDC_GetSelfSyncMode(
		unsigned long			nDeviceNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetRandomTriggerEnable(
		unsigned long nDeviceNo,
		unsigned long nChildNo,
		BOOL *pEnable,
		unsigned long *pErrorCode
		);

unsigned long WINAPI
PDC_GetMaxRandomTriggerCount(
		unsigned long nDeviceNo,
		unsigned long nChildNo,
		unsigned long *pMaxRandomCount,
		unsigned long *pErrorCode
		);

unsigned long WINAPI PDC_GetMaxRandomEndlessTriggerCount(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long *pMaxRandomCount,
	unsigned long *pErrorCode
	);


unsigned long WINAPI
PDC_GetLowFrameRateMode(
		unsigned long nDeviceNo,
		unsigned long *pMode,
		unsigned long *pErrorCode
		);

unsigned long WINAPI PDC_GetAccelerationSensorError(
		unsigned long nDeviceNo,
		unsigned long *pErrorNumber,
		unsigned long *pErrorCode
);


/*
 *	Set Device status
 */
unsigned long WINAPI
PDC_SetActiveChild(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetStatus(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetRecReady(
		unsigned long			nDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetEndless(
		unsigned long			nDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_TriggerIn(
		unsigned long			nDeviceNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetShutterLockMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetResolutionLockMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetPartitionIncMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetKeyPadLock(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetVideoOutMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetExternalInMode(
		unsigned long			nDeviceNo,
		unsigned long			nPort,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetExternalOutMode(
		unsigned long			nDeviceNo,
		unsigned long			nPort,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetIRIG(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetIRIGSampleMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
);


unsigned long WINAPI
PDC_SetMCDL(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetADC(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetADCRange(
		unsigned long			nDeviceNo,
		unsigned long			nADCChannel,
		unsigned long			nMode,
		unsigned long			*pErrorCode
	);

unsigned long WINAPI
PDC_SetIRIGOffset(
		unsigned long			nDeviceNo,
		long					nValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetRecordRate(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nRate,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetTriggerMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			nAFrames,
		unsigned long			nRFrames,
		unsigned long			nRCount,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetResolution(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nWidth,
		unsigned long			nHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetResolutionROI(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nWidth,
		unsigned long			nHeight,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetShutterSpeedFps(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nFps,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetCurrentPartition(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSensorGainMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSensorGammaMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetColorTempMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			nR,
		unsigned long			nG,
		unsigned long			nB,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSoftColorTempMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			nR,
		unsigned long			nG,
		unsigned long			nB,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetAutoExposure(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetLUTMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetDSShutterMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetDSShutterValue(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetEdgeEnhanceMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetShadingMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetPixelGainMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetTransferOption(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			n8BitSel,
		unsigned long			nBayer,
		unsigned long			nInterleave,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_EraseVariableChannel(
		unsigned long			nDeviceNo,
		unsigned long			nChannel,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetVariableChannel(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nChannel,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetVariableChannelInfo(
		unsigned long			nDeviceNo,
		unsigned long			nChannel,
		unsigned long			nRate,
		unsigned long			nWidth,
		unsigned long			nHeight,
		unsigned long			nXPos,
		unsigned long			nYPos,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetAutoExposureInfo(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nWidth,
		unsigned long			nHeight,
		unsigned long			nXPos,
		unsigned long			nYPos,
		unsigned long			nValue,
		unsigned long			nRange,
		unsigned long			nLimit,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetLUTUserParams(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nLUTMode,
		PPDC_LUT_PARAMS			pParams,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_CreatePixelGainData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		void					*pSrc,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetPixelGainData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		void					*pSrc,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetLUTUser(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetDelay(
		unsigned long			nDeviceNo,
		unsigned long			nSignal,
		unsigned long			nValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetColorEnhanceMode(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetDownloadMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetLowLightMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetProgSwitchMode(
		unsigned long			nDeviceNo,
		unsigned long			nSwitchNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSyncOutTimes(
		unsigned long			nDeviceNo,
		unsigned long			nRatio,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetStore(
		unsigned long			nDeviceNo,
		unsigned long			nNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetEthernetInfo(
		unsigned long			nDeviceNo,
		unsigned long			nTarget,
		unsigned long			nValue,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetIRIGPhaseLock(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetHighSpeedMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetBurstTransfer(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetHeadExchange(
		unsigned long			nDeviceNo,
		unsigned long			nNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_SetLiveResolutionMode( 
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetColorType(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetBitDepth(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					nDepth,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetBitDepth2(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		char					nDepth,
		unsigned long			nBitSel,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetCameraCommandBaudRate(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nRate,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSegmentPosition(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nXPos,
		unsigned long			nYPos,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSyncPriority(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetDeviceID(
		unsigned long			nDeviceNo,
		unsigned long			nID,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetVideoOutSignal(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetVideoOutSignalEnable(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetVideoOutHDSDI(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetRecordingType(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetAutoPlay(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetFactoryDefaults(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetStorePreset(
		unsigned long			nDeviceNo,
		unsigned long			nNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetInstructionSet(
		unsigned long			nDeviceNo,
		unsigned long			nInstSetCode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_SetLEDMode(
		unsigned long			nDeviceNo,
		unsigned long			nLEDMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_SetBatteryPowerMode(
		unsigned long			nDeviceNo,
		unsigned long			nBattery,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetBatteryFunction(
		unsigned long nDeviceNo,
		unsigned long nValue,
		unsigned long *pErrorCode
		);

unsigned long WINAPI
PDC_SetKeyPadCommand(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetShadingType(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetBlackClipLevel(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetExposeExtension(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetImageTrigger(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetImageTriggerInfo(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nWidth,
		unsigned long			nHeight,
		unsigned long			nXPos,
		unsigned long			nYPos,
		unsigned long			nValue,
		unsigned long			nRange,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetRTC(
		unsigned long			nDeviceNo,
		unsigned long			nYear,
		unsigned long			nMonth,
		unsigned long			nDay,
		unsigned long			nHour,
		unsigned long			nMinute,
		unsigned long			nSecond,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetLensControlData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nSendDataSize,
		char					*pSendData,
		unsigned long			*pRecvDataSize,
		char					*pRecvData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetMemoryModePartition(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_SetGEtherTransferMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_SetMechaShutterMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetMechaShutterFunction(
		unsigned long			nDeviceNo,
		unsigned long			nValue,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_SetLowFrameRateMode(
		unsigned long nDeviceNo,
		unsigned long nMode,
		unsigned long *pErrorCode
		);

/*	Fan control	*/
unsigned long WINAPI
PDC_SetFanCtrl(
		unsigned long			nDeviceNo,
		unsigned long			nValue,
		unsigned long			*pErrorCode
		);

/*	SD card control	*/
unsigned long WINAPI
PDC_SetSdCardMemoryMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSdCardFormatRequest(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSdCardCancelRequest(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSdCardResetRequest(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_SetSdCardSaveRequest(
		unsigned long			nDeviceNo,
		unsigned long			nSlotNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetHeadLedLaser(
		unsigned long 			nDeviceNo,
		unsigned long 			nChildNo,
		unsigned long 			nLedStatus,
		unsigned long 			nLaserStatus,
		unsigned long 			*pErrorCode
		);

unsigned long WINAPI
PDC_SetFourThirdsLensControlData(
		unsigned long 			nDeviceNo,
		unsigned long 			nChildNo,
		unsigned char 			nCommandType,
		unsigned char 			nCommandCode,
		unsigned char 			nParam1,
		unsigned char 			nParam2,
		unsigned long 			nSendDataSize,
		char 					*pSendData,
		unsigned long 			*pRecvDataSize,
		char 					*pRecvData,
		unsigned long 			*pResult,
		unsigned long 			*pErrorCode
		);

unsigned long WINAPI
PDC_SetSelfSyncMode(
		unsigned long			nDeviceNo,
		unsigned long			nMode,
		unsigned long			*pErrorCode
		);

/*
 *	Get Image
 */
unsigned long WINAPI
PDC_GetLiveImageData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nBitDepth,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLiveImageAddress(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		void					**pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemImageData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			nBitDepth,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemImageDataStart(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			nBitDepth,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemImageDataEnd(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nBitDepth,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemImageAddress(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		void					**pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemIRIGData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		PPDC_IRIG_INFO			pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemMCDLData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		PPDC_MCDL_INFO			pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemIRIGandMCDLData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			nFrameNum,
		PPDC_IRIGMCDL_INFO		pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemMCDLByteData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			nFrameNum,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemADCByteData(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			nFrameNum,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetFastDriveADCByteData(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	long nFrameNo,
	unsigned long nFrameNum,
	void *pData,
	unsigned long *pErrorCode);

unsigned long WINAPI
PDC_GetFastDriveMemBufUseByteData(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	long nFrameNo,
	unsigned long nFrameNum,
	void *pData,
	unsigned long *pErrorCode);

unsigned long WINAPI
PDC_GetMemAutoExposureDataFps(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		PPDC_AUTO_EXPOSURE_INFO	pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemAutoExposureDataNsec(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			nFrameNum,
		PPDC_AUTO_EXPOSURE_INFO	pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_DrawLiveImage(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		HDC						hDC,
		unsigned long			nDisplayMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_DrawMemImage(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		HDC						hDC,
		unsigned long			nDisplayMode,
		long					nFrameNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLiveMemImageData(
						unsigned long			nDeviceNo,
						unsigned long			nChildNo,
						unsigned long			nBitDepth,
						void					*pData,
						unsigned long			*pErrorCode
						);

/*
 *	FPGA Setting
 */
unsigned long WINAPI
PDC_FPGAConfigA(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCSTR					lpszFileName,
		unsigned long			nProgramMode,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_FPGAConfigW(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCWSTR					lpszFileName,
		unsigned long			nProgramMode,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_FPGAConfig  PDC_FPGAConfigW
#else
#define PDC_FPGAConfig  PDC_FPGAConfigA
#endif // !UNICODE

unsigned long WINAPI
PDC_GetFPGAStatus(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pStatus,
		unsigned long 			*pBytesCompleted,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_LoadFPGAConfigFileA(
		unsigned long	nDeviceNo,
		LPCSTR			lpszPath,
		unsigned char	*pInfo,
		unsigned long	nSize,
		unsigned long	*pErrorCode
		);
unsigned long WINAPI
PDC_LoadFPGAConfigFileW(
		unsigned long	nDeviceNo,
		LPCWSTR			lpszPath,
		unsigned char	*pInfo,
		unsigned long	nSize,
		unsigned long	*pErrorCode
		);
#ifdef UNICODE
#define PDC_LoadFPGAConfigFile  PDC_LoadFPGAConfigFileW
#else
#define PDC_LoadFPGAConfigFile  PDC_LoadFPGAConfigFileA
#endif // !UNICODE

unsigned long WINAPI
PDC_SetReset_FPGA(
		unsigned long nDeviceNo,
		unsigned long nEnable,
		unsigned long nFPGAType,
		unsigned long *pErrorCode
		);

/*
 *	File Save
 */
unsigned long WINAPI
PDC_BMPFileSaveA(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCSTR					lpszFileName,
		long					nFrameNo,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_BMPFileSaveW(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCWSTR					lpszFileName,
		long					nFrameNo,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_BMPFileSave  PDC_BMPFileSaveW
#else
#define PDC_BMPFileSave  PDC_BMPFileSaveA
#endif // !UNICODE

unsigned long WINAPI
PDC_AVIFileSaveOpenA(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCSTR					lpszFileName,
		long					nRate,
		unsigned long			nShowCompressDlg,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_AVIFileSaveOpenW(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCWSTR					lpszFileName,
		long					nRate,
		unsigned long			nShowCompressDlg,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_AVIFileSaveOpen  PDC_AVIFileSaveOpenW
#else
#define PDC_AVIFileSaveOpen  PDC_AVIFileSaveOpenA
#endif // !UNICODE

unsigned long WINAPI
PDC_AVIFileSave(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			*pSize,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_AVIFileSaveClose(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_MRAWFileSaveOpenA(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCSTR					lpszFileName,
		unsigned long			nMRawBitDepth,
		long					nMaxFrameNum,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_MRAWFileSaveOpenW(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCWSTR					lpszFileName,
		unsigned long			nMRawBitDepth,
		long					nMaxFrameNum,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_MRAWFileSaveOpen  PDC_MRAWFileSaveOpenW
#else
#define PDC_MRAWFileSaveOpen  PDC_MRAWFileSaveOpenA
#endif // !UNICODE

unsigned long WINAPI 
PDC_MRAWFileSave(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_MRAWFileSaveClose(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo, 
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_MRAWFileSaveOpenExA(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCSTR					lpszFileName,
		unsigned long			nMRawBitDepth,
		long					nMaxFrameNum,
		long					nConnectMode2P,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_MRAWFileSaveOpenExW(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		LPCWSTR					lpszFileName,
		unsigned long			nMRawBitDepth,
		long					nMaxFrameNum,
		long					nConnectMode2P,
		unsigned long			*pErrorCode
		);
#ifdef UNICODE
#define PDC_MRAWFileSaveOpenEx PDC_MRAWFileSaveOpenExW
#else
#define PDC_MRAWFileSaveOpenEx PDC_MRAWFileSaveOpenExA
#endif // !UNICODE

unsigned long WINAPI
PDC_MRAWFileSaveStartEx(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nStartFrameNum,
		long					nEndFrameNum,
		unsigned long			*pErrorCode
);

unsigned long WINAPI
PDC_MRAWFileSaveCancelEx(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_MRAWFileSaveStatusEx(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					*pSaving,
		long					*pFrameNum,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_MRAWFileSaveCloseEx(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pErrorCode
);

/*
 *	File Load
 */
unsigned long WINAPI 
PDC_MRAWFileLoadOpenA(
		LPCSTR					lpszFileName,
		PPDC_IMAGE_BUFF_INFO	pInfo,
		unsigned long			nMRawBitDepth,
		unsigned long			*pFileNo,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_MRAWFileLoadOpenW(
		LPCWSTR					lpszFileName,
		PPDC_IMAGE_BUFF_INFO	pInfo,
		unsigned long			nMRawBitDepth,
		unsigned long			*pFileNo,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_MRAWFileLoadOpen  PDC_MRAWFileLoadOpenW
#else
#define PDC_MRAWFileLoadOpen  PDC_MRAWFileLoadOpenA
#endif // !UNICODE

unsigned long WINAPI 
PDC_MRAWFileLoadOpen2A(
		LPCSTR					lpszFileName,
		PPDC_IMAGE_BUFF_INFO	pInfo,
		unsigned long			nMRawBitDepth,
		unsigned long			*pSessionNo,
		PPDC_ORG_IMAGE_INFO		pOrgInfo,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_MRAWFileLoadOpen2W(
		LPCWSTR					lpszFileName,
		PPDC_IMAGE_BUFF_INFO	pInfo,
		unsigned long			nMRawBitDepth,
		unsigned long			*pSessionNo,
		PPDC_ORG_IMAGE_INFO		pOrgInfo,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_MRAWFileLoadOpen2  PDC_MRAWFileLoadOpen2W
#else
#define PDC_MRAWFileLoadOpen2  PDC_MRAWFileLoadOpen2A
#endif // !UNICODE

unsigned long WINAPI 
PDC_MRAWFileLoad(
		unsigned long			nFileNo,
		long					nFrame,
		void					*pBuff,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_MRAWFileLoadClose(
		unsigned long			nFileNo,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_RAWFileLoadA(
		LPCSTR					lpszFileName,
		PPDC_IMAGE_BUFF_INFO	pInfo,
		unsigned long			nRawBitDepth,
		void					*pBuff,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_RAWFileLoadW(
		LPCWSTR					lpszFileName,
		PPDC_IMAGE_BUFF_INFO	pInfo,
		unsigned long			nRawBitDepth,
		void					*pBuff,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_RAWFileLoad  PDC_RAWFileLoadW
#else
#define PDC_RAWFileLoad  PDC_RAWFileLoadA
#endif // !UNICODE

unsigned long WINAPI 
PDC_RAWFileLoad2A(
		LPCSTR					lpszFileName,
		PPDC_IMAGE_BUFF_INFO	pInfo,
		unsigned long			nRawBitDepth,
		void					*pBuff,
		PPDC_ORG_IMAGE_INFO		pOrgInfo,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_RAWFileLoad2W(
		LPCWSTR					lpszFileName,
		PPDC_IMAGE_BUFF_INFO	pInfo,
		unsigned long			nRawBitDepth,
		void					*pBuff,
		PPDC_ORG_IMAGE_INFO		pOrgInfo,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_RAWFileLoad2  PDC_RAWFileLoad2W
#else
#define PDC_RAWFileLoad2  PDC_RAWFileLoad2A
#endif // !UNICODE

/*
 *	Camera Link Control
 */
unsigned long WINAPI
PDC_ReadCameraDefFileA(
		unsigned long			nDeviceNo,
		LPCSTR					lpszFileName,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_ReadCameraDefFileW(
		unsigned long			nDeviceNo,
		LPCWSTR					lpszFileName,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_ReadCameraDefFile  PDC_ReadCameraDefFileW
#else
#define PDC_ReadCameraDefFile  PDC_ReadCameraDefFileA
#endif // !UNICODE

unsigned long WINAPI
PDC_WriteCameraDefFileA(
		unsigned long			nDeviceNo,
		LPCSTR					lpszFileName,
		unsigned long			*pErrorCode
		);
unsigned long WINAPI
PDC_WriteCameraDefFileW(
		unsigned long			nDeviceNo,
		LPCWSTR					lpszFileName,
		unsigned long			*pErrorCode
);
#ifdef UNICODE
#define PDC_WriteCameraDefFile  PDC_WriteCameraDefFileW
#else
#define PDC_WriteCameraDefFile  PDC_WriteCameraDefFileA
#endif // !UNICODE

unsigned long WINAPI
PDC_SetCameraCommand(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned char			*pBuf,
		unsigned long			nSize,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_GetCameraLinkStatus(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pMode,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_GetBayerAlignment(
		unsigned long			nDeviceNo,
		unsigned long			*pBayerAlign,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI 
PDC_SetBayerAlignment(
		unsigned long			nDeviceNo,
		unsigned long			nBayerAlign,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemory(
		unsigned long			nDeviceNo,
		unsigned long			*pBlockAvailable,
		unsigned long			*pBlockReserved,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetMemory(
		unsigned long			nDeviceNo,
		unsigned long			nOption,
		unsigned long			nBlocks,
		unsigned long			nFramePerBlock,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetNumofDropFrame(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pDropFrame,
		unsigned long			*pErrorCode
		);

#if _MSC_VER < 1300
unsigned long WINAPI
PDC_GetMemoryInfo(
		unsigned long nDeviceNo,
		unsigned __int64 *pAvailableMemory,
		unsigned __int64 *pReservedMemory,
		unsigned long *pErrorCode
		);
#else
unsigned long WINAPI
PDC_GetMemoryInfo(
		unsigned long nDeviceNo,
		unsigned long long		*pAvailableMemory,
		unsigned long long		*pReservedMemory,
		unsigned long			*pErrorCode
		);
#endif

unsigned long WINAPI
PDC_GetDropFrameList(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		PPDC_DROP_FRAME_LIST	pList,
		unsigned long			*pSize,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetLiveImageAddress2(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			*pFrameNo,
		void					**pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemImageData2(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			nBitDepth,
		unsigned long			nPort,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemImageDataStart2(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		long					nFrameNo,
		unsigned long			nBitDepth,
		unsigned long			nPort,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_GetMemImageDataEnd2(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nBitDepth,
		unsigned long			nPort,
		void					*pData,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_SetMemImageMode(
		unsigned long nMemImageMode,
		unsigned long *pErrorCode
);

unsigned long WINAPI
PDC_MultipleGetMemImageDataInit(
		unsigned long			nDeviceNo,
		unsigned long			nChildNo,
		unsigned long			nBitDepth,
		PPDC_SAVE_FRAME_INFO	pFrameInfo,
		long					nConnectMode2P,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI
PDC_MultipleGetMemImageData(
		unsigned long	nDeviceNo,
		unsigned long	nChildNo,
		long			nFrameNo,
		void			*pData,
		unsigned long   *pErrorCode
		);

unsigned long WINAPI
PDC_MultipleGetMemImageDataCancel(
		unsigned long nDeviceNo,
		unsigned long nChildNo,
		unsigned long *pErrorCode
);

unsigned long WINAPI
PDC_MultipleGetMemImageDataExit(
		unsigned long nDeviceNo,
		unsigned long nChildNo,
		unsigned long *pErrorCode
);

/*
 *	Image Processing
 */
unsigned long WINAPI
PDC_ConvertBayerImageData(
		PPDC_IMAGE_BUFF_INFO	pInfo, 
		PPDC_BAYER_CONVERT_INFO	pBayerInfo,
		void					*pSrc,
		void					*pDes,
		unsigned long			*pErrorCode
		);

unsigned long WINAPI PDC_SetRandomTriggerEnable(
		unsigned long nDeviceNo,
		unsigned long nMode,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetResetTriggerExposeDelay(
	unsigned long nDeviceNo,
	unsigned long *pValue,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetDeadTimeValue(
	unsigned long nDeviceNo,
	unsigned long *pValue,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetStraddlingDelay(
	unsigned long nDeviceNo,
	unsigned long *pPulse1,
	unsigned long *pPulse2,
	unsigned long *pErrorCode);

unsigned long WINAPI
PDC_GetExposurePosition(unsigned long nDeviceNo,
unsigned long *pValue,
unsigned long *pErrorCode);

unsigned long WINAPI
PDC_GetVSyncExposeDeviation(unsigned long nDeviceNo,
long *pValue,
unsigned long *pErrorCode);

// PIV
unsigned long WINAPI PDC_GetLiveResetMode(
		unsigned long nDeviceNo,
		unsigned long *pLiveMode,
		unsigned long *pResetMode,
		unsigned long *pTotalFrame,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_SetLiveResetMode(
		unsigned long nDeviceNo,
		unsigned long nLiveMode,
		unsigned long nResetMode,
		unsigned long nTotalFrame,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetLiveResetImage(
		unsigned long nDeviceNo,
		unsigned long nChildNo,
		unsigned long nBitDepth,
		void *pData1,
		void *pData2,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetReadAheadTransfer(
		unsigned long nDeviceNo,
		unsigned long *pMode,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_SetReadAheadTransfer(
		unsigned long nDeviceNo,
		unsigned long nChildNo,
		unsigned long nMode,
		long		  nStartFrame,
		long		  nEndFrame,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetDirectRecordFastDrive(
		unsigned long nDeviceNo,
		unsigned long *pMode,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_SetDirectRecordFastDrive(
		unsigned long nDeviceNo,
		unsigned long nMode,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveRecordInfo(
		unsigned long nDeviceNo,
		unsigned long nSlotNo,
		unsigned long nDataNo,
		void *pRecInfo,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveImage(
		unsigned long nDeviceNo,
		unsigned long nSlotNo,
		unsigned long nDataNo,
		unsigned long nFrameNo,
		unsigned long nInterleave,
		void *pData,
		unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveLut(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	void *pLutR,
	void *pLutG,
	void *pLutB,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveIrig(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	long nFrameNo,
	PPDC_IRIG_INFO pData,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveAutoExposure(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	long nFrameNo,
	PPDC_AUTO_EXPOSURE_INFO pData,
	unsigned long *pErrorCode);


unsigned long WINAPI PDC_GetFastDriveTemperatureType(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	unsigned long* pType,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveTemperature(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	long nFrameNo,
	PVOID pData,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_FastDriveOpen(
	unsigned long nDeviceNo,
	unsigned long *pDataNum,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_FastDriveClose(
	unsigned long nDeviceNo,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveActivityRatio(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	double *pActivityRatio,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveTotalWrittenSize(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long long *pWrittenSize,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveImageDataStart(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	unsigned long nFrameNo,
	unsigned long nInterleave,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveImageDataEnd(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	unsigned long nFrameNo,
	unsigned long nInterleave,
	void *pData,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveDataCount(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long long *pDataCount,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_EnterFastDrivePassword(unsigned long nDeviceNo,
	char *pPassword,
	unsigned long *pErrorCode);
unsigned long WINAPI PDC_SetFastDrivePassword(unsigned long nDeviceNo,
	char *pOldPassword,
	char *pNewPassword,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetFastDriveAcceleration(unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	long nFrameNo,
	PVOID pData,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetDeviceSeries(
	unsigned long nDeviceNo,
	unsigned long *pSeries,
	unsigned long *pErrorCode); 
unsigned long WINAPI PDC_GetStorageDownloadMode(
	unsigned long nDeviceNo,
	unsigned long *pMode,
	unsigned long *pErrorCode);
unsigned long WINAPI PDC_SetStorageDownloadMode(
	unsigned long nDeviceNo,
	unsigned long nMode,
	unsigned long *pErrorCode);
unsigned long WINAPI PDC_GetProgSwitchCount(
	unsigned long nDeviceNo,
	unsigned long *pCount,
	unsigned long *pErrorCode);
unsigned long WINAPI PDC_GetLowLightMode2(
	unsigned long nDeviceNo,
	unsigned long *pMode,
	unsigned long *pErrorCode);
unsigned long WINAPI PDC_SetLowLightMode2(
	unsigned long nDeviceNo,
	unsigned long nMode,
	unsigned long *pErrorCode);
unsigned long WINAPI PDC_GetPixelGainDataSize(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long *pSize,
	unsigned long *pErrorCode
);
unsigned long WINAPI PDC_GetPixelGainDataMode3Size(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long *pSize,
	unsigned long *pErrorCode);
unsigned long WINAPI PDC_GetDSShutterLimit(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long *pLimit,
	unsigned long *pErrorCode
	);

unsigned long WINAPI
PDC_SetWiFiScanRequest(
	unsigned long	nDeviceNo,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetWiFiScanCount(
	unsigned long	nDeviceNo,
	unsigned long	*pCount,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetWiFiScanInfoA(
	unsigned long	nDeviceNo,
	unsigned long	nSelectNo,
	PPDC_WIFI_INFOA	pInfo,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetWiFiScanInfoW(
	unsigned long	nDeviceNo,
	unsigned long	nSelectNo,
	PPDC_WIFI_INFOW	pInfo,
	unsigned long	*pErrorCode
	);

#ifdef UNICODE
#define PDC_GetWiFiScanInfo  PDC_GetWiFiScanInfoW
#else
#define PDC_GetWiFiScanInfo  PDC_GetWiFiScanInfoA
#endif // !UNICODE

unsigned long WINAPI
PDC_SetWiFiPassword(
	unsigned long	nDeviceNo,
	unsigned long	nSelectNo,
	char*			strPassword,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_SetWiFiConnect(
	unsigned long	nDeviceNo,
	unsigned long	nSelectNo,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_SetWiFiDisconnect(
	unsigned long	nDeviceNo,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetBatteryInfo(
	unsigned long		nDeviceNo,
	PPDC_BATTERY_INFO	pInfo,
	unsigned long		*pErrorCode
	);

unsigned long WINAPI
PDC_GetShutdownBatterySupply(
	unsigned long	nDeviceNo,
	unsigned long	*pMode,
	unsigned long	*pTime,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_SetShutdownBatterySupply(
	unsigned long	nDeviceNo,
	unsigned long	nMode,
	unsigned long	nTime,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetShutdownBatterySupplyRange(
	unsigned long	nDeviceNo,
	unsigned long	*pMinTime,
	unsigned long	*pMaxTime,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetMediaSaveBatterySupply(
	unsigned long	nDeviceNo,
	unsigned long	*pMode,
	unsigned long	*pTime,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_SetMediaSaveBatterySupply(
	unsigned long	nDeviceNo,
	unsigned long	nMode,
	unsigned long	nTime,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetMediaSaveBatterySupplyRange(
	unsigned long	nDeviceNo,
	unsigned long	*pMinTime,
	unsigned long	*pMaxTime,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetAutoPowerWhenSupply(
	unsigned long	nDeviceNo,
	unsigned long	*pMode,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_SetAutoPowerWhenSupply(
	unsigned long	nDeviceNo,
	unsigned long	nMode,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetPartitionLock(
	unsigned long	nDeviceNo,
	unsigned long	*pMode,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_SetPartitionLock(
	unsigned long	nDeviceNo,
	unsigned long	nMode,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_SetShutdownCamera(
	unsigned long	nDeviceNo,
	unsigned long	nMode,
	unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_GetAccelerationTrigger(
	unsigned long	nDeviceNo,
	unsigned long	*pMode,
	unsigned long	*pAcceleration,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_SetAccelerationTrigger(
	unsigned long	nDeviceNo,
	unsigned long	nMode,
	unsigned long	nAcceleration,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI
PDC_GetAccelerationTriggerLimit(
unsigned long	nDeviceNo,
unsigned long	*pLimitLower,
unsigned long	*pLimitUpper,
unsigned long	*pStep,
unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_GetAccelerationTriggerTime(
unsigned long	nDeviceNo,
unsigned long	*pTime,
unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_SetAccelerationTriggerTime(
unsigned long	nDeviceNo,
unsigned long	nTime,
unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_GetAccelerationTriggerTimeLimit(
unsigned long	nDeviceNo,
unsigned long	*pLimitLower,
unsigned long	*pLimitUpper,
unsigned long	*pStep,
unsigned long	*pErrorCode
);

unsigned long WINAPI
PDC_SetExternalOutSignalSpan(
	unsigned long nDeviceNo,
	unsigned long nPort,
	char nFlag,
	unsigned long* pErrorCode
	);

unsigned long WINAPI
PDC_GetExternalOutSignalSpan(
	unsigned long nDeviceNo,
	unsigned long nPort,
	char* pFlag,
	unsigned long* pErrorCode
	);

unsigned long WINAPI
PDC_ReqExternalOutSignalSpan(
	unsigned long nDeviceNo,
	unsigned long nPort,
	char* pFlag,
	unsigned long* pErrorCode
	);

unsigned long WINAPI
PDC_SetFanRecReadyStop(
	unsigned long nDeviceNo,
	char nFlag,
	unsigned long* pErrorCode
	);
unsigned long WINAPI
PDC_GetFanRecReadyStop(
	unsigned long nDeviceNo,
	char* pFlag,
	unsigned long* pErrorCode
	);
unsigned long WINAPI
PDC_ReqFanRecReadyStop(
	unsigned long nDeviceNo,
	char* pFlag,
	unsigned long* pErrorCode
	);

unsigned long WINAPI
PDC_GetLensParam(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long nType,
	unsigned long nOption,
	long* pParam,
	unsigned long* pErrorCode
	);

unsigned long WINAPI
PDC_ReqLensParam(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long nType,
	unsigned long nOption,
	long* pParam,
	unsigned long* pErrorCode
	);

unsigned long WINAPI
PDC_SetLensParam(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long nType,
	unsigned long nOption,
	long nParam,
	unsigned long* pErrorCode
);

unsigned long WINAPI PDC_GetTemperature(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long nChannel,
	long* pValue,
	unsigned long *pErrorCode
	);

unsigned long WINAPI PDC_GetMemTemperatureData(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	void *pData,
	long nFrameNo,
	unsigned long nFrameCount,
	unsigned long *pErrorCode
	);

unsigned long WINAPI PDC_GetMemTemperatureType(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long* pType,
	unsigned long* pErrorCode
	);

unsigned long WINAPI PDC_GetTemperatureTypeList(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long *pSize,
	unsigned long *pList,
	unsigned long *pErrorCode
	);			

/*
* for MH6
*/
unsigned long WINAPI PDC_GetWarningTemperature(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	char * pFlag,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetWarningCableCutting(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	char * pFlag,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetTriggerNoiseFilter(
	unsigned long nDeviceNo,
	unsigned long *pMode,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_SetTriggerNoiseFilter(
	unsigned long nDeviceNo,
	unsigned long nMode,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetTriggerNoiseFilterWidth(
	unsigned long nDeviceNo,
	unsigned long *pWidth,
	unsigned long *pLimitUpper,
	unsigned long *pLimitLower,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_SetTriggerNoiseFilterWidth(
	unsigned long nDeviceNo,
	unsigned long nWidth,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetVDAIOType(
	unsigned long nDeviceNo,
	unsigned long nPort,
	unsigned long *pValue,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_SetVDAIOType(
	unsigned long nDeviceNo,
	unsigned long nPort,
	unsigned long nValue,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetMemoryShare(
	unsigned long nDeviceNo,
	unsigned long *pMode,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_SetMemoryShare(
	unsigned long nDeviceNo,
	unsigned long nMode,
	unsigned long *pErrorCode);

unsigned long WINAPI PDC_GetMemAccelerationData(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	void *pData,
	long nFrameNo,
	unsigned long nFrameCount,
	unsigned long *pErrorCode
	);

unsigned long WINAPI PDC_GetVideoOSDCrosshairMode(
	unsigned long	nDeviceNo,
	unsigned long*	nMode,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI PDC_GetSerialNumber(
	unsigned long nChildNo,
	unsigned long nDeviceNo,
	unsigned long long *pSerialNumber,
	unsigned long *pErrorCode);
    
unsigned long WINAPI PDC_SetVideoOSDCrosshairMode(
	unsigned long	nDeviceNo,
	unsigned long	nMode,
	unsigned long	*pErrorCode
	);

unsigned long WINAPI PDC_GetShutterSpeedPrecision(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	long *pValue,
	unsigned long *pErrorCode
	);

unsigned long WINAPI PDC_GetFastDriveShutterSpeedPrecision(
	unsigned long nDeviceNo,
	unsigned long nSlotNo,
	unsigned long nDataNo,
	long *pValue,
	unsigned long *pErrorCode
	);

unsigned long WINAPI PDC_GetAutoExposureLimit(
	unsigned long nDeviceNo,
	unsigned long nChildNo,
	unsigned long *pValue,
	unsigned long *pErrorCode
	);

unsigned long WINAPI PDC_StorageIsFunction(
	unsigned long nDeviceCode,
	unsigned long nOption,
	unsigned long nFunction,
	char *pFlag,
	unsigned long *pErrorCode
	);
/*
* for FAST Drive
*/
unsigned long WINAPI PFDC_GetValidDrives(unsigned long *pDrives, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_OpenDrive(unsigned long nDriveNo, unsigned long *pNumOfData, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_CloseDrive(unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetDriveName(unsigned long nDriveNo, char *pName, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetRecordInfo(unsigned long nDataNo, PDC_RECORD_INFO *pRecordInfo, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetLUTData(unsigned long nDataNo, void *pLUTR, void *pLUTG, void *pLUTB, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetExposeTimeData(unsigned long nDataNo, unsigned long *pExposeTimeData, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_SetDataName(unsigned long nDataNo, char *pName, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetImageData(unsigned long nDataNo, long nFrameNo, long nInterleave, void *pImageData, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetIRIGInfo(unsigned long nDataNo, long nFrameNo, PDC_IRIG_INFO *pIRIGInfo, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetRecOnCmdTrigFrames(unsigned long nDataNo, unsigned long *pBuff, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetAutoExposureFps(unsigned long nDataNo, long nFrameNo, PPDC_AUTO_EXPOSURE_INFO pAE, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetAutoExposureNsec(unsigned long nDataNo, long nFrameNo, PPDC_AUTO_EXPOSURE_INFO pAE, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_StartImageBuffering(unsigned long nDataNo, unsigned long *pErrorCode);
void WINAPI PFDC_FinishImageBuffering(void);
unsigned long WINAPI PFDC_GetActivityRatio(double *pActivityRatio, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetTotalWrittenSize(unsigned long long *pTotalWrittenSize, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_FormatDrive(unsigned long *pErrorCode);
unsigned long WINAPI PFDC_TestDrive(unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetTemperatureType(unsigned long nDataNo, unsigned long* pType, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetTemperature(unsigned long nDataNo, long nFrameNo, void* pData, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetShutterSpeedPrecision(unsigned long nDataNo, long* pValue, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetADCByteData(unsigned long nDataNo, long nFrameNo, unsigned long nFrameNum, void* pData, unsigned long *pErrorCode);
unsigned long WINAPI PFDC_GetAdcInfo(unsigned long nDataNo, unsigned long* pNumberOfChannel, unsigned long* pSamplePerFrame, unsigned long *pErrorCode);

/*
* for SD Card
*/
unsigned long WINAPI PSDC_GetValidDrives(unsigned long *pDrives, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_OpenDrive(unsigned long nDriveNo, unsigned long *pNumOfData, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_CloseDrive(unsigned long *pErrorCode);
unsigned long WINAPI PSDC_GetRecordInfo(unsigned long nDataNo, PDC_RECORD_INFO *pRecordInfo, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_GetLUTData(unsigned long nDataNo, void *pLUTR, void *pLUTG, void *pLUTB, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_GetExposeTimeData(unsigned long nDataNo, unsigned long *pExposeTimeData, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_GetRecOnCmdTrigFrames(unsigned long nDataNo, unsigned long *pBuff, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_GetImageData(unsigned long nDataNo, long nFrameNo, long nInterleave, void *pImageData, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_GetIRIGInfo(unsigned long nDataNo, long nFrameNo, PDC_IRIG_INFO *pIRIGInfo, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_GetAutoExposureFps(unsigned long nDataNo, long nFrameNo, PDC_AUTO_EXPOSURE_INFO *pAEInfo, unsigned long *pErrorCode);
unsigned long WINAPI PSDC_GetAutoExposureNsec(unsigned long nDataNo, long nFrameNo, PDC_AUTO_EXPOSURE_INFO *pAEInfo, unsigned long *pErrorCode);


#ifdef	__cplusplus
}
#endif	/*	__cplusplus	*/

#endif	/*	_PDC_FUNC_H_	*/

